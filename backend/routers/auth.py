from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.schemas import UserRegister, UserLogin, UserOut

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash="hashed_" + user_data.password,
        phone=user_data.phone,
        location=user_data.location or "Chennai, India"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=UserOut)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        # Create guest/demo user if not found for seamless testing
        user = User(
            full_name=login_data.email.split("@")[0].capitalize(),
            email=login_data.email,
            password_hash="demo_hash",
            location="Chennai, India"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

@router.get("/me", response_model=UserOut)
def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        user = User(
            full_name="Karthik R.",
            email="karthik@example.com",
            location="Chennai, Tamil Nadu"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
