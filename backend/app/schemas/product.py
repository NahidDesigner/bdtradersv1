from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    title_bn: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    description_bn: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    discount_price: Optional[Decimal] = Field(None, ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_in_stock: bool = Field(default=True)
    track_inventory: bool = Field(default=True)
    images: List[str] = Field(default_factory=list)
    slug: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    is_published: bool = Field(default=True)
    is_featured: bool = Field(default=False)


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    title_bn: Optional[str] = None
    description: Optional[str] = None
    description_bn: Optional[str] = None
    price: Optional[Decimal] = None
    discount_price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    is_in_stock: Optional[bool] = None
    track_inventory: Optional[bool] = None
    images: Optional[List[str]] = None
    slug: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    uuid: str
    title: str
    title_bn: Optional[str]
    description: Optional[str]
    description_bn: Optional[str]
    price: Decimal
    discount_price: Optional[Decimal]
    stock_quantity: int
    is_in_stock: bool
    images: List[str]
    slug: Optional[str]
    is_published: bool
    is_featured: bool
    
    class Config:
        from_attributes = True

