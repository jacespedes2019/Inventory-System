"""
File: auth.py
Description: Authentication and authorization API endpoints.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Register new users with email, password, and role.
- Authenticate users and return JWT tokens.
- Protect endpoints with JWT Bearer authentication.

Notes:
- Passwords are hashed using bcrypt before storage.
- JWT tokens embed `sub` (user id) and `role`.
- Tokens are required for accessing protected routes.
""" 

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return UserService(db).register(data)

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and return a JWT access token (contains 'role')."""
    token = UserService(db).login(payload.email, payload.password)
    return Token(access_token=token)