from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product_repo import ProductRepository
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

class ProductService:
    """Business logic for product operations."""
    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)

    def list(self, q: Optional[str] = None) -> List[ProductOut]:
        """List products, optionally filtered by q."""
        items = self.repo.list(q=q)
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