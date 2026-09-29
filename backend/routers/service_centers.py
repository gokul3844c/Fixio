import math
import uuid
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import ServiceCenter, Review, User, Appointment
from backend.schemas import ServiceCenterOut, AppointmentCreate, ReviewCreate, ReviewOut
from backend.auth_utils import get_current_user

router = APIRouter(prefix="/api/service-centers", tags=["Service Centers"])

def calculate_haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)

@router.get("", response_model=List[ServiceCenterOut])
def list_service_centers(
    category: Optional[str] = None,
    city: Optional[str] = None,
    q: Optional[str] = None,
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None,
    open_now: Optional[bool] = None,
    min_rating: Optional[float] = None,
    verified_only: Optional[bool] = None,
    sort_by: Optional[str] = "distance", # distance, rating
    db: Session = Depends(get_db)
):
    query = db.query(ServiceCenter)

    if category and category.lower() != "all":
        query = query.filter(ServiceCenter.category.ilike(f"%{category}%"))

    if city and city.strip():
        query = query.filter(
            (ServiceCenter.city.ilike(f"%{city}%")) |
            (ServiceCenter.address.ilike(f"%{city}%"))
        )

    if q and q.strip():
        query = query.filter(
            (ServiceCenter.store_name.ilike(f"%{q}%")) |
            (ServiceCenter.address.ilike(f"%{q}%")) |
            (ServiceCenter.category.ilike(f"%{q}%"))
        )

    if open_now is True:
        query = query.filter(ServiceCenter.is_open_now == True)

    if min_rating is not None:
        query = query.filter(ServiceCenter.rating >= min_rating)

    if verified_only is True:
        query = query.filter(ServiceCenter.is_authorized == True)

    centers = query.all()

    # Calculate dynamic spatial distance if user coordinates provided (default center: Chennai 13.0827, 80.2707)
    origin_lat = user_lat if user_lat is not None else 13.0827
    origin_lng = user_lng if user_lng is not None else 80.2707

    for center in centers:
        if center.lat and center.lng:
            center.distance_km = calculate_haversine_km(origin_lat, origin_lng, center.lat, center.lng)

    if sort_by == "rating":
        centers.sort(key=lambda x: x.rating, reverse=True)
    else:
        centers.sort(key=lambda x: x.distance_km)

    return centers

@router.get("/{center_id}", response_model=ServiceCenterOut)
def get_service_center(center_id: int, db: Session = Depends(get_db)):
    sc = db.query(ServiceCenter).filter(ServiceCenter.id == center_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Service center not found")
    return sc

@router.post("/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def submit_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sc = db.query(ServiceCenter).filter(ServiceCenter.id == review_data.service_center_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Service center not found")

    if review_data.rating < 1 or review_data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5 stars")

    if not review_data.comment or not review_data.comment.strip():
        raise HTTPException(status_code=400, detail="Review comment cannot be empty")

    existing = db.query(Review).filter(
        Review.service_center_id == review_data.service_center_id,
        Review.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You have already submitted a review for this service center.")

    new_review = Review(
        service_center_id=review_data.service_center_id,
        user_id=current_user.id,
        user_name=current_user.full_name,
        rating=review_data.rating,
        comment=review_data.comment.strip(),
        verified_job=review_data.verified_job if review_data.verified_job is not None else True
    )

    db.add(new_review)

    all_reviews = db.query(Review).filter(Review.service_center_id == review_data.service_center_id).all()
    total_rating = sum(r.rating for r in all_reviews) + review_data.rating
    sc.review_count = len(all_reviews) + 1
    sc.rating = round(total_rating / sc.review_count, 1)

    db.commit()
    db.refresh(new_review)

    return new_review

@router.post("/book-appointment")
def book_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    store = db.query(ServiceCenter).filter(ServiceCenter.id == appointment.store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Service center not found")

    code = f"APT-{appointment.store_id}-{uuid.uuid4().hex[:6].upper()}"

    new_appointment = Appointment(
        appointment_code=code,
        user_id=current_user.id,
        service_center_id=appointment.store_id,
        preferred_date=appointment.preferred_date,
        preferred_time=appointment.preferred_time,
        notes=appointment.notes,
        status="Confirmed"
    )

    db.add(new_appointment)
    db.commit()

    return {
        "success": True,
        "message": f"Appointment booked successfully with {store.store_name} for {appointment.preferred_date} at {appointment.preferred_time}.",
        "appointment_id": code
    }

