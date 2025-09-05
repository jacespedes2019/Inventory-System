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

    def create(self, email: str, password_hash: str) -> User:
        """Create and persist a user."""
        user = User(email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user