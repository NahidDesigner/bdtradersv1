from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
import uuid


class OrderStatus(str, enum.Enum):
    PENDING = "pending"  # পেন্ডিং
    CONFIRMED = "confirmed"  # কনফার্মড
    SHIPPED = "shipped"  # শিপড
    DELIVERED = "delivered"  # ডেলিভার্ড
    CANCELLED = "cancelled"  # বাতিল


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Order number (human-readable)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # Customer info
    customer_name = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_email = Column(String(255), nullable=True)
    customer_address = Column(Text, nullable=False)
    
    # Order details
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, index=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    shipping_cost = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    
    # Shipping
    shipping_class_id = Column(Integer, ForeignKey("shipping_classes.id"), nullable=True)
    shipping_notes = Column(Text, nullable=True)
    
    # Payment
    payment_method = Column(String(50), default="cod")  # cod, bank_transfer, etc.
    payment_status = Column(String(50), default="pending")  # pending, paid, failed
    
    # Facebook Pixel tracking
    fb_pixel_id = Column(String(50), nullable=True)
    fb_event_id = Column(String(100), nullable=True)  # For deduplication
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="orders")
    shipping_class = relationship("ShippingClass", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Product snapshot (in case product is deleted/modified)
    product_title = Column(String(500), nullable=False)
    product_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

