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