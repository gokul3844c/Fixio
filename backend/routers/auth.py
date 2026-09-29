import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from backend.database import get_db
from backend.models import User
from backend.schemas import UserRegister, UserLogin, GoogleLogin, UserOut, Token
from backend.auth_utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if not user_data.email or not user_data.password or not user_data.full_name:
        raise HTTPException(status_code=400, detail="Name, email, and password are required")
    
    email_clean = user_data.email.strip().lower()
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    new_user = User(
        full_name=user_data.full_name.strip(),
        email=email_clean,
        password_hash=hash_password(user_data.password),
        phone=user_data.phone,
        location=user_data.location or "Chennai, India"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.id, "email": new_user.email})
    user_out = UserOut.from_orm(new_user)
    return Token(access_token=access_token, token_type="bearer", user=user_out)

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    if not login_data.email or not login_data.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    email_clean = login_data.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.id, "email": user.email})
    user_out = UserOut.from_orm(user)
    return Token(access_token=access_token, token_type="bearer", user=user_out)

@router.post("/google", response_model=Token)
def google_sign_in(payload: GoogleLogin, db: Session = Depends(get_db)):
    raw_token = payload.credential or payload.token
    if not raw_token:
        raise HTTPException(status_code=400, detail="Google credential token missing")

    try:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        # Verify RSA signature and claims against Google public certs
        claims = id_token.verify_oauth2_token(
            raw_token,
            google_requests.Request(),
            audience=client_id if client_id else None
        )

        email = claims.get('email')
        name = claims.get('name') or claims.get('given_name') or (email.split('@')[0] if email else "Google User")
        picture = claims.get('picture')

        if not email:
            raise HTTPException(status_code=400, detail="Could not retrieve email from Google Sign-In")

        email_clean = email.strip().lower()

        # Find or create user
        user = db.query(User).filter(User.email == email_clean).first()
        if not user:
            user = User(
                full_name=name,
                email=email_clean,
                avatar_url=picture or "/assets/avatars/default.jpg",
                password_hash=None, # Google authenticated user
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        elif picture and user.avatar_url == "/assets/avatars/default.jpg":
            user.avatar_url = picture
            db.commit()

        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        user_out = UserOut.from_orm(user)
        return Token(access_token=access_token, token_type="bearer", user=user_out)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google Sign-In verification failed: {str(e)}")

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.from_orm(current_user)

