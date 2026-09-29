from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, DamageReport, Notification
from backend.schemas import UserOut, DamageReportOut
from backend.auth_utils import get_current_user

router = APIRouter(prefix="/api/user", tags=["User Dashboard"])

@router.get("/dashboard")
def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_scans = db.query(DamageReport).filter(DamageReport.user_id == current_user.id).count()
    issues_found = db.query(DamageReport).filter(
        DamageReport.user_id == current_user.id,
        DamageReport.damage_status.ilike("%Damaged%")
    ).count()
    repaired_count = db.query(DamageReport).filter(
        DamageReport.user_id == current_user.id,
        DamageReport.damage_status.ilike("%Repaired%")
    ).count()
    in_progress_count = db.query(DamageReport).filter(
        DamageReport.user_id == current_user.id,
        DamageReport.damage_status.ilike("%Progress%")
    ).count()

    recent_scans = db.query(DamageReport).filter(
        DamageReport.user_id == current_user.id
    ).order_by(DamageReport.created_at.desc()).limit(5).all()
    
    notifications = db.query(Notification).order_by(Notification.timestamp.desc()).limit(10).all()

    return {
        "user": current_user,
        "metrics": {
            "total_scans": total_scans,
            "issues_found": issues_found,
            "repaired_count": repaired_count,
            "in_progress_count": in_progress_count
        },
        "recent_scans": recent_scans,
        "notifications": notifications
    }
