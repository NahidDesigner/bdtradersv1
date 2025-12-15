from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Dict, List
from app.core.database import get_db
from app.models.order import Order, OrderStatus, OrderItem
from app.models.product import Product
from app.api.v1.tenants import get_current_user_id
from app.api.v1.products import get_tenant_from_request
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/dashboard", response_model=Dict)
async def get_dashboard_stats(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get dashboard analytics"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Total orders
    total_orders_result = await db.execute(
        select(func.count(Order.id)).where(Order.tenant_id == tenant.id)
    )
    total_orders = total_orders_result.scalar() or 0
    
    # Total revenue
    total_revenue_result = await db.execute(
        select(func.sum(Order.total)).where(
            Order.tenant_id == tenant.id,
            Order.status != OrderStatus.CANCELLED
        )
    )
    total_revenue = total_revenue_result.scalar() or 0
    
    # Pending orders
    pending_orders_result = await db.execute(
        select(func.count(Order.id)).where(
            Order.tenant_id == tenant.id,
            Order.status == OrderStatus.PENDING
        )
    )
    pending_orders = pending_orders_result.scalar() or 0
    
    # Today's orders
    today = datetime.utcnow().date()
    today_orders_result = await db.execute(
        select(func.count(Order.id)).where(
            Order.tenant_id == tenant.id,
            func.date(Order.created_at) == today
        )
    )
    today_orders = today_orders_result.scalar() or 0
    
    # Today's revenue
    today_revenue_result = await db.execute(
        select(func.sum(Order.total)).where(
            Order.tenant_id == tenant.id,
            func.date(Order.created_at) == today,
            Order.status != OrderStatus.CANCELLED
        )
    )
    today_revenue = today_revenue_result.scalar() or 0
    
    # Conversion rate (orders / visitors - simplified)
    # In production, track actual visitors
    conversion_rate = 0.0  # Placeholder
    
    # Top products
    top_products_result = await db.execute(
        select(
            Product.id,
            Product.title,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.subtotal).label("total_revenue")
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.id)
        .where(
            Order.tenant_id == tenant.id,
            Order.status != OrderStatus.CANCELLED
        )
        .group_by(Product.id, Product.title)
        .order_by(desc("total_sold"))
        .limit(5)
    )
    top_products = [
        {
            "id": row.id,
            "title": row.title,
            "total_sold": row.total_sold,
            "total_revenue": float(row.total_revenue)
        }
        for row in top_products_result
    ]
    
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "pending_orders": pending_orders,
        "today_orders": today_orders,
        "today_revenue": float(today_revenue),
        "conversion_rate": conversion_rate,
        "top_products": top_products
    }


@router.get("/orders/trend", response_model=List[Dict])
async def get_orders_trend(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    days: int = 7
):
    """Get orders trend over time"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Get orders for last N days
    start_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(
            func.date(Order.created_at).label("date"),
            func.count(Order.id).label("count"),
            func.sum(Order.total).label("revenue")
        )
        .where(
            Order.tenant_id == tenant.id,
            Order.created_at >= start_date
        )
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
    )
    
    trends = [
        {
            "date": str(row.date),
            "orders": row.count,
            "revenue": float(row.revenue or 0)
        }
        for row in result
    ]
    
    return trends

