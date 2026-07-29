import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import DamageReport, User, Component
from backend.schemas import DamageReportOut
from backend.ai_engine import AIElectronicsEngine

router = APIRouter(prefix="/api/scan", tags=["Scan"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("", response_model=DamageReportOut)
async def scan_image(
    file: UploadFile = File(...),
    device_name: str = Form("Motherboard PCB Rev 3.2"),
    db: Session = Depends(get_db)
):
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        relative_path = f"/static/uploads/{file.filename}"

        # Analyze with AI vision engine
        analysis = AIElectronicsEngine.analyze_pcb_image(file_path, file.filename)

        # Get demo user
        user = db.query(User).first()
        user_id = user.id if user else None

        # Check matching component
        comp = db.query(Component).filter(Component.part_number == analysis["part_number"]).first()
        comp_id = comp.id if comp else None

        # Create DamageReport record
        report = DamageReport(
            user_id=user_id,
            device_name=device_name or analysis["device_name"],
            component_id=comp_id,
            component_name=analysis["component_name"],
            part_number=analysis["part_number"],
            image_path=relative_path,
            damage_status=analysis["damage_status"],
            confidence_percentage=analysis["confidence_percentage"],
            severity_level=analysis["severity_level"],
            estimated_repair_cost=analysis["estimated_repair_cost"],
            estimated_repair_time=analysis["estimated_repair_time"],
            bounding_boxes=analysis["bounding_boxes"],
            damage_cause=analysis["damage_cause"],
            repair_steps_summary=analysis["repair_steps_summary"],
            datasheet_url=analysis["datasheet_url"]
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@router.get("/{report_id}", response_model=DamageReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not report:
        # Return default latest report if not found
        report = db.query(DamageReport).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("", response_model=list[DamageReportOut])
def list_reports(db: Session = Depends(get_db)):
    reports = db.query(DamageReport).order_by(DamageReport.created_at.desc()).all()
    return reports
