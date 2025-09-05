from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    """Data access layer for Product entity."""
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, q: Optional[str] = None) -> List[Product]:
        """Return products filtered by name (ILIKE) if q is provided."""
        stmt = select(Product)
        if q:
            stmt = stmt.where(Product.name.ilike(f"%{q}%"))
        stmt = stmt.order_by(Product.name.asc())
        return list(self.db.execute(stmt).scalars().all())

    def get(self, product_id: int) -> Optional[Product]:
        """Return a product by id or None."""
        return self.db.get(Product, product_id)

    def create(self, data: ProductCreate) -> Product:
        """Create and persist a product."""
        obj = Product(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, product_id: int, data: ProductUpdate) -> Optional[Product]:
        """Update a product if exists; return updated or None."""
        obj = self.get(product_id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, product_id: int) -> bool:
        """Delete a product by id. Return True if deleted."""
        obj = self.get(product_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True