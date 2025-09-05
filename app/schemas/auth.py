from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """JWT access token response."""
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    """Login credentials."""
    email: EmailStr
    password: str