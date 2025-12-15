from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from decimal import Decimal


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")
    brand_color: Optional[str] = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")
    currency: str = Field(default="BDT", max_length=3)
    default_language: str = Field(default="bn", pattern="^(bn|en)$")
    
    @validator("slug")
    def validate_slug(cls, v):
        # Ensure slug is URL-safe
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Slug must contain only alphanumeric characters, hyphens, and underscores")
        return v.lower()


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    brand_color: Optional[str] = None
    currency: Optional[str] = None
    default_language: Optional[str] = None
    whatsapp_number: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None
    enable_cod: Optional[bool] = None
    enable_facebook_pixel: Optional[bool] = None
    facebook_pixel_id: Optional[str] = None
    facebook_access_token: Optional[str] = None
    email_notifications: Optional[bool] = None
    whatsapp_notifications: Optional[bool] = None
    notification_email: Optional[str] = None
    notification_whatsapp: Optional[str] = None
    settings: Optional[Dict] = None


class TenantResponse(BaseModel):
    id: int
    uuid: str
    slug: str
    name: str
    logo: Optional[str]
    brand_color: str
    currency: str
    default_language: str
    whatsapp_number: Optional[str]
    support_phone: Optional[str]
    enable_cod: bool
    enable_facebook_pixel: bool
    
    class Config:
        from_attributes = True

