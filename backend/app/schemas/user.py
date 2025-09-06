"""
File: user.py
Description: Pydantic schemas for user-related requests and responses.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Define request models (UserCreate, LoginRequest).
- Define response models (UserOut, Token).
- Ensure data validation for authentication and user registration.

Notes:
- Passwords are required only for registration and login.
- Token schema provides access_token and token_type.
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr

# Define allowed role literals; extend as needed.
RoleLiteral = Literal["admin", "user"]

class UserBase(BaseModel):
    """Base fields shared by user schemas."""
    email: EmailStr

class UserCreate(UserBase):
    """Payload for user registration (role optional; defaults to 'user')."""
    password: str
    role: Optional[RoleLiteral] = "user"

class UserOut(UserBase):
    """Public representation of a user."""
    id: int
    role: RoleLiteral
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)