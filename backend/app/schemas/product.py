"""
File: product.py
Description: Pydantic schemas for product-related requests and responses.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Define ProductCreate, ProductUpdate for input validation.
- Define ProductOut for response serialization.
- Ensure consistent typing for product fields.

Notes:
- Pydantic automatically converts numeric strings to floats where required.
- Optional fields are allowed in updates.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    """Base fields shared by product schemas."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    image_url: Optional[str] = Field(None, max_length=512)

class ProductCreate(ProductBase):
    """Payload for product creation."""
    pass

class ProductUpdate(BaseModel):
    """Payload for partial product update."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = Field(None, max_length=512)

class ProductOut(ProductBase):
    """Public representation of a product."""
    id: int
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)