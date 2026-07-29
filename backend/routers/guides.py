from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import RepairGuide
from backend.schemas import RepairGuideOut

router = APIRouter(prefix="/api/guides", tags=["Repair Guides"])

@router.get("", response_model=List[RepairGuideOut])
def list_guides(db: Session = Depends(get_db)):
    return db.query(RepairGuide).all()

@router.get("/{guide_id}", response_model=RepairGuideOut)
def get_guide(guide_id: int, db: Session = Depends(get_db)):
    guide = db.query(RepairGuide).filter(RepairGuide.id == guide_id).first()
    if not guide:
        guide = db.query(RepairGuide).first()
        if not guide:
            raise HTTPException(status_code=404, detail="Repair guide not found")
    return guide
