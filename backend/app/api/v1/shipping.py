from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.schemas.shipping import ShippingClassCreate, ShippingClassUpdate, ShippingClassResponse
from app.models.shipping import ShippingClass
from app.api.v1.tenants import get_current_user_id
from app.api.v1.products import get_tenant_from_request

router = APIRouter()


@router.post("", response_model=ShippingClassResponse, status_code=status.HTTP_201_CREATED)
async def create_shipping_class(
    shipping_data: ShippingClassCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Create shipping class"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    shipping_class = ShippingClass(
        **shipping_data.dict(),
        tenant_id=tenant.id
    )
    
    db.add(shipping_class)
    await db.commit()
    await db.refresh(shipping_class)
    
    return shipping_class


@router.get("", response_model=List[ShippingClassResponse])
async def list_shipping_classes(
    request: Request,
    db: AsyncSession = Depends(get_db),
    active_only: bool = False
):
    """List shipping classes (tenant-scoped)"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    query = select(ShippingClass).where(ShippingClass.tenant_id == tenant.id)
    
    if active_only:
        query = query.where(ShippingClass.is_active == True)
    
    query = query.order_by(ShippingClass.sort_order, ShippingClass.name)
    
    result = await db.execute(query)
    shipping_classes = result.scalars().all()
    
    return shipping_classes


@router.get("/{shipping_id}", response_model=ShippingClassResponse)
async def get_shipping_class(
    shipping_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Get shipping class by ID"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    result = await db.execute(
        select(ShippingClass).where(
            ShippingClass.id == shipping_id,
            ShippingClass.tenant_id == tenant.id
        )
    )
    shipping_class = result.scalar_one_or_none()
    
    if not shipping_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping class not found"
        )
    
    return shipping_class


@router.put("/{shipping_id}", response_model=ShippingClassResponse)
async def update_shipping_class(
    shipping_id: int,
    shipping_data: ShippingClassUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update shipping class"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    result = await db.execute(
        select(ShippingClass).where(
            ShippingClass.id == shipping_id,
            ShippingClass.tenant_id == tenant.id
        )
    )
    shipping_class = result.scalar_one_or_none()
    
    if not shipping_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping class not found"
        )
    
    # Update fields
    update_data = shipping_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shipping_class, key, value)
    
    await db.commit()
    await db.refresh(shipping_class)
    
    return shipping_class


@router.delete("/{shipping_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipping_class(
    shipping_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Delete shipping class"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    result = await db.execute(
        select(ShippingClass).where(
            ShippingClass.id == shipping_id,
            ShippingClass.tenant_id == tenant.id
        )
    )
    shipping_class = result.scalar_one_or_none()
    
    if not shipping_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping class not found"
        )
    
    await db.delete(shipping_class)
    await db.commit()
    
    return None

