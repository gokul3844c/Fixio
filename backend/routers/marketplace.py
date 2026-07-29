from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import Product
from backend.schemas import ProductOut

router = APIRouter(prefix="/api/marketplace", tags=["Marketplace"])

@router.get("", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category and category.lower() != "all":
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if q:
        query = query.filter(
            (Product.name.ilike(f"%{q}%")) |
            (Product.part_number.ilike(f"%{q}%")) |
            (Product.compatibility_info.ilike(f"%{q}%"))
        )
    return query.all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod
