"""
File: user_repo.py
Description: Repository for querying and persisting User entities.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Provide database operations for the User entity.
- Encapsulate logic to fetch, create, and search users by email or id.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User

class UserRepository:
    """Data access layer for User entity."""
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        """Return user by email or None."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, password_hash: str, role: str = "user") -> User:
        """Create and persist a user with the given role."""
        user = User(email=email, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user