from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import decode_access_token
from fastapi import Header

router = APIRouter()


async def get_current_user_id(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Extract user ID from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return user_id


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: TenantCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Create a new tenant/store"""
    # Check if slug already exists
    result = await db.execute(
        select(Tenant).where(Tenant.slug == tenant_data.slug)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Store slug already exists"
        )
    
    # Create tenant
    tenant = Tenant(
        **tenant_data.dict(),
        owner_id=user_id
    )
    
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    
    return tenant


@router.get("", response_model=List[TenantResponse])
async def list_tenants(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """List all tenants owned by current user"""
    result = await db.execute(
        select(Tenant).where(Tenant.owner_id == user_id)
    )
    tenants = result.scalars().all()
    return tenants


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get tenant by ID"""
    result = await db.execute(
        select(Tenant).where(
            Tenant.id == tenant_id,
            Tenant.owner_id == user_id
        )
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return tenant


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update tenant"""
    result = await db.execute(
        select(Tenant).where(
            Tenant.id == tenant_id,
            Tenant.owner_id == user_id
        )
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Update fields
    update_data = tenant_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tenant, key, value)
    
    await db.commit()
    await db.refresh(tenant)
    
    return tenant


@router.get("/slug/{slug}", response_model=TenantResponse)
async def get_tenant_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get tenant by slug (public endpoint for store pages)"""
    result = await db.execute(
        select(Tenant).where(
            Tenant.slug == slug,
            Tenant.is_active == True
        )
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    return tenant

