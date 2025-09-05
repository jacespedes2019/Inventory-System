from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, asc, desc

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

# Map logical sort field names to model columns
_SORT_COLUMNS = {
    "name": Product.name,
    "price": Product.price,
    "quantity": Product.quantity,
    "updated_at": Product.updated_at,
}


class ProductRepository:
    """Data access layer for Product entity."""
    def __init__(self, db: Session) -> None:
        self.db = db

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
    ) -> List[Product]:
        """
        Return products that match optional search, filtering and sorting.
        - Search: 'q' performs an ILIKE on name.
        - Filtering:
            * min_price/max_price on Product.price
            * min_qty on Product.quantity
            * has_image: True -> image_url IS NOT NULL AND <> ''; False -> image_url IS NULL OR ''
        - Sorting: by one of _SORT_COLUMNS and asc/desc.
        """
        stmt = select(Product)
        conds = []

        # --- Search ---
        if q:
            conds.append(Product.name.ilike(f"%{q}%"))

        # --- Filters ---
        if min_price is not None:
            conds.append(Product.price >= min_price)
        if max_price is not None:
            conds.append(Product.price <= max_price)
        if min_qty is not None:
            conds.append(Product.quantity >= min_qty)
        if has_image is True:
            conds.append(and_(Product.image_url.is_not(None), Product.image_url != ""))
        elif has_image is False:
            conds.append(or_(Product.image_url.is_(None), Product.image_url == ""))

        if conds:
            stmt = stmt.where(and_(*conds))

        # --- Sorting ---
        sort_col = _SORT_COLUMNS.get(sort_by, Product.name)
        stmt = stmt.order_by(asc(sort_col) if sort_dir == "asc" else desc(sort_col))

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