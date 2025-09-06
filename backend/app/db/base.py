"""
File: base.py
Description: Central metadata for SQLAlchemy models.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Collect SQLAlchemy Base class for model declarations.
- Allow Base.metadata.create_all() to create all tables.

Notes:
- All models (User, Product) must import Base from this module.
- Required for testing (pytest) to generate tables dynamically.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""
    pass