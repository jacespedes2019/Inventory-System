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
        """Register a new user if email is not taken."""
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = hash_password(data.password)
        user = self.repo.create(email=data.email, password_hash=hashed)
        return UserOut.model_validate(user)

    def login(self, email: str, password: str) -> str:
        """Validate credentials and return a JWT token."""
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(subject=str(user.id))