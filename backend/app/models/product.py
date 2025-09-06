"""
File: product.py
Description: SQLAlchemy model for inventory products.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Define `products` table with fields id, name, description, price, quantity, image_url, updated_at.
- Represent products in the inventory system.

Notes:
- Price is stored as numeric (float).
- updated_at auto-refreshes on modification.
"""

from sqlalchemy import String, Integer, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import datetime

from app.db.base import Base

class Product(Base):
    """Product entity for inventory management."""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    price: Mapped["Decimal"] = mapped_column(Numeric(12, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str] = mapped_column(String(512), nullable=True)
    updated_at: Mapped["datetime"] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )