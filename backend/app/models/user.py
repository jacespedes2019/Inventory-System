from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    """User entity used for authentication and authorization."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # Store role as a short string; typical values: "admin", "user"
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
    created_at: Mapped["datetime"] = mapped_column(DateTime, server_default=func.now(), nullable=False)