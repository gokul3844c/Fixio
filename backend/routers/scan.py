import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from PIL import Image

from backend.database import get_db
from backend.models import DamageReport, User, Component
from backend.ai_engine import FixioAIEngine
from backend.auth_utils import get_current_user

router = APIRouter(prefix="/api/scan", tags=["Scan"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("")
async def scan_image(
    file: UploadFile = File(...),
    device_name: str = Form("Electronic Component / PCB"),
    mode: str = Form("datasheet"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: JPG, PNG, WEBP, BMP."
        )

    # Validate file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum limit of 10MB."
        )

    safe_filename = f"scan_{uuid.uuid4().hex[:8]}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Validate binary magic bytes with Pillow
        try:
            with Image.open(file_path) as img:
                img.verify()
        except Exception:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is not a valid image payload or is corrupted."
            )

        relative_path = f"/static/uploads/{safe_filename}"

        # Perform AI electronic component & OCR analysis
        result = FixioAIEngine.analyze_uploaded_image(file_path, file.filename, db=db)
        result["image_url"] = relative_path

        # Database record for scan history tracking
        ident = result.get("identification", {})
        comp_data = result.get("component_data", {})
        part_num = ident.get("part_number") or "UNCONFIRMED"

        comp_id = None
        if part_num and part_num != "UNCONFIRMED":
            comp = db.query(Component).filter(
                Component.part_number.ilike(part_num)
            ).first()
            if comp:
                comp_id = comp.id

        report = DamageReport(
            scan_id=result.get("scan_id", f"scan_{uuid.uuid4().hex[:8]}"),
            user_id=current_user.id,
            mode="component_datasheet",
            device_name=device_name or "Electronic Component / PCB",
            component_id=comp_id,
            component_name=comp_data.get("name", "Electronic Component"),
            manufacturer=ident.get("manufacturer") or "Semiconductor OEM",
            part_number=part_num,
            image_path=relative_path,
            damage_status=f"Status: {ident.get('status', 'unknown').capitalize()}",
            confidence_percentage=0.0, # Evidence-based: 0/null to prevent fake confidence scores
            severity_level="info",
            estimated_repair_cost="N/A",
            estimated_repair_time="N/A",
            bounding_boxes=[],
            issues_json=[],
            disclaimer="Component specifications retrieved from OEM datasheet database. Verify pinouts before soldering.",
            damage_cause=result.get("message") or f"Identified component part number: {part_num}",
            repair_steps_summary=result.get("recommendations", []),
            datasheet_url=comp_data.get("datasheet_url")
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        result["id"] = report.id
        result["report_id"] = report.id
        result["mode"] = report.mode
        result["issues_json"] = result.get("issues_json", [])
        result["bounding_boxes"] = result.get("bounding_boxes", [])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Component scan failed: {str(e)}")

@router.get("/{report_id}")
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Scan report not found.")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied. You do not own this scan report.")
    return report

@router.get("")
def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(DamageReport).filter(
        DamageReport.user_id == current_user.id
    ).order_by(DamageReport.created_at.desc()).all()
    return reports
