"""
File: deps.py
Description: Dependency functions for FastAPI routes.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Provide database session dependency (get_db).
- Extract current user id and role from Bearer JWT (get_current_identity).
- Enforce role-based access using require_roles dependency.

Notes:
- Invalid or missing tokens raise HTTP 401.
- Unauthorized roles raise HTTP 403.
"""

from fastapi import HTTPException, Security, status, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal

bearer_scheme = HTTPBearer(auto_error=True)

def get_db():
    """Yield a DB session per request and close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_identity(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> tuple[int, str]:
    """
    Decode JWT from Bearer token and return (user_id, role).
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        sub = payload.get("sub")
        role = payload.get("role")
        if sub is None or role is None:
            raise ValueError("Invalid token payload")
        return int(sub), role
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def require_roles(*allowed_roles: str):
    """
    Dependency factory that enforces role-based access.
    """
    def _dep(identity: tuple[int, str] = Depends(get_current_identity)) -> tuple[int, str]:
        user_id, role = identity
        if allowed_roles and role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return identity
    return _dep