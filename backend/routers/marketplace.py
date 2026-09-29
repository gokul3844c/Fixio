from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import Product, User
from backend.schemas import ProductOut, ProductCreate
from backend.auth_utils import get_current_user

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

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    prod: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    price_fmt = prod.price_formatted or f"${prod.price:.2f}"
    new_product = Product(
        name=prod.name,
        part_number=prod.part_number,
        category=prod.category,
        price=prod.price,
        price_formatted=price_fmt,
        stock_status=prod.stock_status or "In Stock",
        stock_quantity=prod.stock_quantity or 100,
        compatibility_info=prod.compatibility_info or "",
        rating=prod.rating or 5.0,
        image_url=prod.image_url or ""
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod
