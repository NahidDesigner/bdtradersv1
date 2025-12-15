from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product
from app.models.tenant import Tenant
from app.api.v1.tenants import get_current_user_id
import re

router = APIRouter()


def get_tenant_from_request(request: Request) -> Optional[Tenant]:
    """Get tenant from request state (set by middleware)"""
    return getattr(request.state, "tenant", None)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Create a new product"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    # Verify user owns the tenant
    if tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Generate slug if not provided
    slug = product_data.slug
    if not slug:
        slug = re.sub(r'[^a-z0-9]+', '-', product_data.title.lower())
        slug = re.sub(r'^-+|-+$', '', slug)
    
    # Check if slug exists
    result = await db.execute(
        select(Product).where(
            Product.tenant_id == tenant.id,
            Product.slug == slug
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        slug = f"{slug}-{product_data.price}"
    
    # Create product
    product = Product(
        **product_data.dict(),
        slug=slug,
        tenant_id=tenant.id
    )
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return product


@router.get("", response_model=List[ProductResponse])
async def list_products(
    request: Request,
    db: AsyncSession = Depends(get_db),
    published_only: bool = True
):
    """List products (tenant-scoped)"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    query = select(Product).where(Product.tenant_id == tenant.id)
    
    if published_only:
        query = query.where(Product.is_published == True)
    
    result = await db.execute(query.order_by(Product.created_at.desc()))
    products = result.scalars().all()
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Get product by ID"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.tenant_id == tenant.id
        )
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(
    slug: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Get product by slug (public endpoint)"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    result = await db.execute(
        select(Product).where(
            Product.slug == slug,
            Product.tenant_id == tenant.id,
            Product.is_published == True
        )
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update product"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.tenant_id == tenant.id
        )
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update fields
    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    await db.commit()
    await db.refresh(product)
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Delete product"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.tenant_id == tenant.id
        )
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    await db.delete(product)
    await db.commit()
    
    return None

