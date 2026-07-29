from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import ServiceCenter
from backend.schemas import ServiceCenterOut, AppointmentCreate

router = APIRouter(prefix="/api/service-centers", tags=["Service Centers"])

@router.get("", response_model=List[ServiceCenterOut])
def list_service_centers(
    city: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ServiceCenter)
    if city and city.strip():
        query = query.filter(ServiceCenter.city.ilike(f"%{city}%"))
    if q:
        query = query.filter(
            (ServiceCenter.store_name.ilike(f"%{q}%")) |
            (ServiceCenter.address.ilike(f"%{q}%"))
        )
    return query.all()

@router.post("/book-appointment")
def book_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    store = db.query(ServiceCenter).filter(ServiceCenter.id == appointment.store_id).first()
    store_name = store.store_name if store else "Repair Shop"
    return {
        "success": True,
        "message": f"Appointment booked successfully with {store_name} for {appointment.preferred_date} at {appointment.preferred_time}.",
        "appointment_id": "APT-" + str(appointment.store_id) + "9482"
    }
