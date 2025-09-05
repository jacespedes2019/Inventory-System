from pydantic import BaseModel, EmailStr
from typing import Literal

RoleLiteral = Literal["admin", "user"]

class Token(BaseModel):
    """JWT access token response."""
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    """Login credentials."""
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    """Decoded JWT payload used internally."""
    sub: str  # user id
    role: RoleLiteral