from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ShippingClassCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_bn: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    cost: Decimal = Field(..., ge=0)
    is_active: bool = Field(default=True)
    sort_order: int = Field(default=0, ge=0)


class ShippingClassUpdate(BaseModel):
    name: Optional[str] = None
    name_bn: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class ShippingClassResponse(BaseModel):
    id: int
    uuid: str
    name: str
    name_bn: Optional[str]
    description: Optional[str]
    cost: Decimal
    is_active: bool
    sort_order: int
    
    class Config:
        from_attributes = True

