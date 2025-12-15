from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Product info
    title = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)  # Bangla title
    description = Column(Text, nullable=True)
    description_bn = Column(Text, nullable=True)  # Bangla description
    
    # Pricing
    price = Column(Numeric(10, 2), nullable=False)
    discount_price = Column(Numeric(10, 2), nullable=True)
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    is_in_stock = Column(Boolean, default=True)
    track_inventory = Column(Boolean, default=True)
    
    # Media
    images = Column(JSON, default=list)  # Array of image URLs
    
    # SEO
    slug = Column(String(500), nullable=True, index=True)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    
    # Status
    is_published = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

