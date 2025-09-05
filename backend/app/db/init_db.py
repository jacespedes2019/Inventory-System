# Lightweight helper to create tables at startup.
from app.db.session import engine
from app.db.base import Base
from app.models import user, product

def init_db() -> None:
    """Create tables if they do not exist (dev/local only)."""
    Base.metadata.create_all(bind=engine)