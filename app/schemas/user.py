from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    """Base fields shared by user schemas."""
    email: EmailStr

class UserCreate(UserBase):
    """Payload for user registration."""
    password: str

class UserOut(UserBase):
    """Public representation of a user."""
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)