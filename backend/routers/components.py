from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import Component
from backend.schemas import ComponentOut

router = APIRouter(prefix="/api/components", tags=["Components"])

@router.get("", response_model=List[ComponentOut])
def list_components(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Component)
    if category and category.lower() != "all":
        query = query.filter(Component.category.ilike(f"%{category}%"))
    if q:
        query = query.filter(
            (Component.name.ilike(f"%{q}%")) |
            (Component.part_number.ilike(f"%{q}%")) |
            (Component.purpose.ilike(f"%{q}%"))
        )
    return query.all()

@router.get("/{component_id}", response_model=ComponentOut)
def get_component(component_id: int, db: Session = Depends(get_db)):
    comp = db.query(Component).filter(Component.id == component_id).first()
    if not comp:
        # Fallback to first component if ID missing
        comp = db.query(Component).first()
        if not comp:
            raise HTTPException(status_code=404, detail="Component not found")
    return comp
