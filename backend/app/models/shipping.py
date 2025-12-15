from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class ShippingClass(Base):
    __tablename__ = "shipping_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    name_bn = Column(String(255), nullable=True)  # Bangla name
    description = Column(Text, nullable=True)
    cost = Column(Numeric(10, 2), nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="shipping_classes")
    orders = relationship("Order", back_populates="shipping_class")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

