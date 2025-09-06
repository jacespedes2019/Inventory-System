"""
File: session.py
Description: SQLAlchemy session and engine configuration.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Create a SQLAlchemy engine using DATABASE_URL from settings.
- Provide a session factory (SessionLocal) for dependency injection.
- Manage database sessions with scoped transactions.

Notes:
- PostgreSQL is the default database for production.
- SQLite in-memory can be used for testing with session overrides.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create a single engine with pre-ping to avoid stale connections
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)