"""
File: product_service.py
Description: Business logic for product management.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Interact with ProductRepository to perform CRUD operations.
- Transform ORM objects into Pydantic models for API responses.
- Handle optional filters and sorting for product listings.

Notes:
- Keeps controllers (routers) clean by separating logic.
- Returns Pydantic models to enforce schema consistency.
"""
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product_repo import ProductRepository
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

# Allowed sort fields and directions
_ALLOWED_SORT_FIELDS = {"name", "price", "quantity", "updated_at"}
_ALLOWED_SORT_DIRS = {"asc", "desc"}

class ProductService:
    """Business logic for product operations."""
    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)

    def list(
        self,
        q: Optional[str] = None,
        *,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_qty: Optional[int] = None,
        has_image: Optional[bool] = None,
        sort_by: str = "name",
        sort_dir: str = "asc",
    ) -> List[ProductOut]:
        """
        List products supporting:
        - search: q (substring match on name, ILIKE)
        - filtering: min_price, max_price, min_qty, has_image
        - sorting: sort_by (name|price|quantity|updated_at), sort_dir (asc|desc)
        """
        # Normalize and validate sorting
        sort_by = (sort_by or "name").lower()
        sort_dir = (sort_dir or "asc").lower()

        if sort_by not in _ALLOWED_SORT_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid sort_by '{sort_by}'. Allowed: {sorted(_ALLOWED_SORT_FIELDS)}",
            )
        if sort_dir not in _ALLOWED_SORT_DIRS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid sort_dir '{sort_dir}'. Allowed: {sorted(_ALLOWED_SORT_DIRS)}",
            )

        items = self.repo.list(
            q=q,
            min_price=min_price,
            max_price=max_price,
            min_qty=min_qty,
            has_image=has_image,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )
        return [ProductOut.model_validate(i) for i in items]

    def get(self, product_id: int) -> ProductOut:
        """Get a single product or raise 404."""
        obj = self.repo.get(product_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductOut.model_validate(obj)

    def create(self, data: ProductCreate) -> ProductOut:
        """Create a new product."""
        obj = self.repo.create(data)
        return ProductOut.model_validate(obj)

    def update(self, product_id: int, data: ProductUpdate) -> ProductOut:
        """Update an existing product or raise 404."""
        obj = self.repo.update(product_id, data)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductOut.model_validate(obj)

    def delete(self, product_id: int) -> None:
        """Delete a product or raise 404."""
        ok = self.repo.delete(product_id)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")