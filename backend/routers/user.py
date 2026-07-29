from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, DamageReport, Notification
from backend.schemas import UserOut, DamageReportOut

router = APIRouter(prefix="/api/user", tags=["User Dashboard"])

@router.get("/dashboard")
def get_user_dashboard(db: Session = Depends(get_db)):
    user = db.query(User).first()

    total_scans = db.query(DamageReport).count()
    issues_found = db.query(DamageReport).filter(DamageReport.damage_status.ilike("%Damaged%")).count()
    repaired_count = 12
    in_progress_count = 4

    recent_scans = db.query(DamageReport).order_by(DamageReport.created_at.desc()).limit(5).all()
    notifications = db.query(Notification).order_by(Notification.timestamp.desc()).all()

    return {
        "user": user,
        "metrics": {
            "total_scans": total_scans or 24,
            "issues_found": issues_found or 18,
            "repaired_count": repaired_count,
            "in_progress_count": in_progress_count
        },
        "recent_scans": recent_scans,
        "notifications": notifications
    }
