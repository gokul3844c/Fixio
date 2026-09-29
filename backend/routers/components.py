from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import Component
from backend.schemas import ComponentOut, DatasheetSearchOut

router = APIRouter(prefix="/api/components", tags=["Components"])

@router.get("/search", response_model=DatasheetSearchOut)
def search_datasheet(
    part_number: str = Query(..., description="Component Part Number to search"),
    db: Session = Depends(get_db)
):
    clean_part = part_number.strip()
    if not clean_part:
        return DatasheetSearchOut(
            found=False,
            message="Please enter a valid part number."
        )

    # Search DB for exact or partial part number / name match
    comp = db.query(Component).filter(
        (Component.part_number.ilike(clean_part)) |
        (Component.part_number.ilike(f"%{clean_part}%")) |
        (Component.name.ilike(f"%{clean_part}%"))
    ).first()

    if comp:
        return DatasheetSearchOut(
            found=True,
            manufacturer=getattr(comp, "manufacturer", None) or "Original Manufacturer",
            part_number=comp.part_number,
            name=comp.name,
            category=comp.category,
            specifications=comp.specifications,
            datasheet_url=comp.datasheet_url,
            confidence_percentage=98.0,
            original_image_url=comp.image_url,
            message=f"Datasheet successfully located for {comp.part_number}."
        )

    # Never invent a part number or fake datasheet
    return DatasheetSearchOut(
        found=False,
        part_number=clean_part,
        confidence_percentage=0.0,
        message=f"No component datasheet found matching part number '{clean_part}'. Please check the part number and try again."
    )

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
        comp = db.query(Component).first()
        if not comp:
            raise HTTPException(status_code=404, detail="Component not found")
    return comp
