"""
File: products.py
Description: Product management API endpoints.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- List products with optional search, filtering, and sorting.
- Retrieve product by id.
- Create, update, and delete products (admin only).
- Integrate with ProductService and ProductRepository.

Notes:
- Endpoints are protected with JWT authentication.
- Role-based restrictions enforced: admin can write, user read-only.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.deps import get_db, require_roles, get_current_identity
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(
    tags=["products"],
    # Any authenticated user can access this router.
    dependencies=[Depends(get_current_identity)],
)

@router.get("/", response_model=List[ProductOut])
def list_products(
    # --- Search ---
    q: Optional[str] = Query(default=None, description="Search by name substring"),
    # --- Filtering ---
    min_price: Optional[float] = Query(default=None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(default=None, ge=0, description="Maximum price"),
    min_qty:   Optional[int]   = Query(default=None, ge=0, description="Minimum quantity"),
    has_image: Optional[bool]  = Query(default=None, description="Filter by having image_url"),
    # --- Sorting ---
    sort_by:   str = Query(default="name", description="Sort field: name|price|quantity|updated_at"),
    sort_dir:  str = Query(default="asc", description="Sort direction: asc|desc"),
    db: Session = Depends(get_db),
):
    """List products with search, filtering and sorting."""
    return ProductService(db).list(
        q=q,
        min_price=min_price,
        max_price=max_price,
        min_qty=min_qty,
        has_image=has_image,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a product by id: allowed for any authenticated role."""
    return ProductService(db).get(product_id)

@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    """Create a new product: admin only."""
    return ProductService(db).create(payload)

@router.put(
    "/{product_id}",
    response_model=ProductOut,
    dependencies=[Depends(require_roles("admin"))],
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing product: admin only."""
    return ProductService(db).update(product_id, payload)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("admin"))],
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """Delete a product: admin only."""
    ProductService(db).delete(product_id)
    return None