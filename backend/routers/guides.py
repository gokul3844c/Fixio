from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import RepairGuide
from backend.schemas import RepairGuideOut

router = APIRouter(prefix="/api/guides", tags=["Repair Guides"])

@router.get("", response_model=List[RepairGuideOut])
def list_guides(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(RepairGuide)
    if category and category.lower() != "all":
        query = query.filter(RepairGuide.category.ilike(f"%{category}%"))
    if q and q.strip():
        query = query.filter(
            (RepairGuide.title.ilike(f"%{q}%")) |
            (RepairGuide.category.ilike(f"%{q}%")) |
            (RepairGuide.short_explanation.ilike(f"%{q}%"))
        )
    return query.all()

@router.get("/match", response_model=List[RepairGuideOut])
def match_guides_for_issue(
    category: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(RepairGuide)

    if category and category.strip():
        query = query.filter(
            (RepairGuide.category.ilike(f"%{category}%")) |
            (RepairGuide.title.ilike(f"%{category}%"))
        )

    if q and q.strip():
        query = query.filter(
            (RepairGuide.title.ilike(f"%{q}%")) |
            (RepairGuide.short_explanation.ilike(f"%{q}%"))
        )

    results = query.all()

    if not results:
        # If no specific category match, return general guides list
        results = db.query(RepairGuide).limit(5).all()

    # Safety enforcement for high-severity or electrical/structural hazards
    if severity and severity.lower() == "high":
        for guide in results:
            if "electrical" in guide.category.lower() or "structural" in guide.category.lower() or "wire" in guide.title.lower():
                guide.when_to_stop = "CRITICAL SAFETY WARNING: High severity electrical hazards or load-bearing structural damage must NOT be attempted as DIY. Turn off main utilities and hire a licensed professional immediately."

    return results

@router.get("/{guide_id}", response_model=RepairGuideOut)
def get_guide(guide_id: int, db: Session = Depends(get_db)):
    guide = db.query(RepairGuide).filter(RepairGuide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Repair guide not found.")
    return guide

