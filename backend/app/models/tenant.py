from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)  # subdomain slug
    name = Column(String(255), nullable=False)
    logo = Column(String(500), nullable=True)
    brand_color = Column(String(7), default="#3B82F6")  # Hex color
    currency = Column(String(3), default="BDT")
    default_language = Column(String(5), default="bn")  # bn or en
    
    # Contact info
    whatsapp_number = Column(String(20), nullable=True)
    support_phone = Column(String(20), nullable=True)
    support_email = Column(String(255), nullable=True)
    
    # Settings
    enable_cod = Column(Boolean, default=True)
    enable_facebook_pixel = Column(Boolean, default=False)
    facebook_pixel_id = Column(String(50), nullable=True)
    facebook_access_token = Column(String(500), nullable=True)  # For Meta CAPI
    
    # Notification settings
    email_notifications = Column(Boolean, default=True)
    whatsapp_notifications = Column(Boolean, default=True)
    notification_email = Column(String(255), nullable=True)
    notification_whatsapp = Column(String(20), nullable=True)
    
    # Metadata
    settings = Column(JSON, default=dict)  # Additional settings
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tenants")
    
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="tenant", cascade="all, delete-orphan")
    shipping_classes = relationship("ShippingClass", back_populates="tenant", cascade="all, delete-orphan")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

