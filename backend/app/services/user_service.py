"""
File: user_service.py
Description: Business logic for user registration and authentication.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Register new users with hashed passwords.
- Authenticate user credentials against database.
- Generate JWT tokens for authenticated users.

Notes:
- Delegates DB operations to SQLAlchemy session.
- Raises exceptions for invalid credentials or duplicate emails.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserOut

class UserService:
    """Business logic for user registration and authentication."""
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    def register(self, data: UserCreate) -> UserOut:
        """Register a new user; role defaults to 'user' unless provided."""
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = hash_password(data.password)
        # persist role
        user = self.repo.create(email=data.email, password_hash=hashed, role=data.role or "user")
        return UserOut.model_validate(user)

    def login(self, email: str, password: str) -> str:
        """Validate credentials and return a JWT token including the user's role."""
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(subject=str(user.id), role=user.role)