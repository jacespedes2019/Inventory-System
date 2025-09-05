from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.deps import get_current_user_id, get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
def list_products(
    q: Optional[str] = Query(default=None, description="Search by name substring"),
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    """List products with optional search."""
    return ProductService(db).list(q=q)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    """Retrieve a product by id."""
    return ProductService(db).get(product_id)

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    """Create a new product."""
    return ProductService(db).create(payload)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    """Update an existing product."""
    return ProductService(db).update(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    """Delete a product."""
    ProductService(db).delete(product_id)
    return None