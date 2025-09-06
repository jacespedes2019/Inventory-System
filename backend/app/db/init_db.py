"""
File: init_db.py
Description: Helper for initializing database schema at application startup.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Create all tables from Base metadata if they do not exist.
- Called during FastAPI startup event.

Notes:
- This is a simple alternative to migrations.
"""

from app.db.session import engine
from app.db.base import Base
from app.models import user, product

def init_db() -> None:
    """Create tables if they do not exist (dev/local only)."""
    Base.metadata.create_all(bind=engine)