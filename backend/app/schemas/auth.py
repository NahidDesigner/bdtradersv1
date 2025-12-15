from pydantic import BaseModel, Field, validator
from typing import Optional


class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    
    @validator("phone")
    def validate_phone(cls, v):
        # Remove spaces, dashes, and ensure it starts with country code or local format
        v = v.replace(" ", "").replace("-", "").replace("+", "")
        if not v.isdigit():
            raise ValueError("Phone number must contain only digits")
        # Bangladesh phone numbers: 01XXXXXXXXX (11 digits) or 8801XXXXXXXXX (13 digits)
        if len(v) < 10 or len(v) > 15:
            raise ValueError("Invalid phone number length")
        return v


class OTPVerify(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    otp: str = Field(..., min_length=4, max_length=6)


class PasswordLogin(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserCreate(BaseModel):
    phone: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    uuid: str
    phone: str
    email: Optional[str]
    full_name: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True

