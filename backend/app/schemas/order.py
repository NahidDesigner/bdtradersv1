from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_phone: str = Field(..., min_length=10, max_length=20)
    customer_email: Optional[str] = None
    customer_address: str = Field(..., min_length=1)
    items: List[OrderItemCreate] = Field(..., min_items=1)
    shipping_class_id: Optional[int] = None
    shipping_notes: Optional[str] = None
    payment_method: str = Field(default="cod")
    notes: Optional[str] = None
    fb_pixel_id: Optional[str] = None
    fb_event_id: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[str] = None
    shipping_notes: Optional[str] = None
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_title: str
    product_price: Decimal
    quantity: int
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    uuid: str
    order_number: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str]
    customer_address: str
    status: OrderStatus
    subtotal: Decimal
    shipping_cost: Decimal
    total: Decimal
    payment_method: str
    payment_status: str
    items: List[OrderItemResponse]
    created_at: str
    
    class Config:
        from_attributes = True

