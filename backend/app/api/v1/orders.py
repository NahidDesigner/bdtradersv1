from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderItemResponse
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.tenant import Tenant
from app.models.shipping import ShippingClass
from app.api.v1.tenants import get_current_user_id
from app.api.v1.products import get_tenant_from_request
from app.services.email import EmailService
from app.services.whatsapp import WhatsAppService
from app.services.facebook_pixel import FacebookPixelService
from decimal import Decimal
import string
import random

router = APIRouter()


def generate_order_number() -> str:
    """Generate unique order number"""
    prefix = "ORD"
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{random_part}"


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Create a new order (public endpoint)"""
    tenant = get_tenant_from_request(request)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    if not tenant.enable_cod and order_data.payment_method == "cod":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cash on delivery not enabled for this store"
        )
    
    # Calculate order totals
    subtotal = Decimal("0")
    order_items_data = []
    
    for item_data in order_data.items:
        # Get product
        result = await db.execute(
            select(Product).where(
                Product.id == item_data.product_id,
                Product.tenant_id == tenant.id,
                Product.is_published == True
            )
        )
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item_data.product_id} not found"
            )
        
        if not product.is_in_stock or (product.track_inventory and product.stock_quantity < item_data.quantity):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.title}"
            )
        
        # Use discount price if available
        price = product.discount_price if product.discount_price else product.price
        item_subtotal = price * item_data.quantity
        subtotal += item_subtotal
        
        order_items_data.append({
            "product": product,
            "quantity": item_data.quantity,
            "price": price,
            "subtotal": item_subtotal
        })
    
    # Get shipping cost
    shipping_cost = Decimal("0")
    shipping_class = None
    if order_data.shipping_class_id:
        result = await db.execute(
            select(ShippingClass).where(
                ShippingClass.id == order_data.shipping_class_id,
                ShippingClass.tenant_id == tenant.id,
                ShippingClass.is_active == True
            )
        )
        shipping_class = result.scalar_one_or_none()
        if shipping_class:
            shipping_cost = shipping_class.cost
    
    total = subtotal + shipping_cost
    
    # Create order
    order = Order(
        tenant_id=tenant.id,
        order_number=generate_order_number(),
        customer_name=order_data.customer_name,
        customer_phone=order_data.customer_phone,
        customer_email=order_data.customer_email,
        customer_address=order_data.customer_address,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        total=total,
        shipping_class_id=order_data.shipping_class_id,
        shipping_notes=order_data.shipping_notes,
        payment_method=order_data.payment_method,
        notes=order_data.notes,
        fb_pixel_id=order_data.fb_pixel_id,
        fb_event_id=order_data.fb_event_id,
        status=OrderStatus.PENDING
    )
    
    db.add(order)
    await db.flush()  # Get order ID
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product"].id,
            product_title=item_data["product"].title,
            product_price=item_data["price"],
            quantity=item_data["quantity"],
            subtotal=item_data["subtotal"]
        )
        db.add(order_item)
        
        # Update product stock
        if item_data["product"].track_inventory:
            item_data["product"].stock_quantity -= item_data["quantity"]
            if item_data["product"].stock_quantity <= 0:
                item_data["product"].is_in_stock = False
    
    await db.commit()
    await db.refresh(order)
    
    # Load order items for response
    result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = result.scalars().all()
    
    # Send notifications in background
    if tenant.email_notifications and tenant.notification_email:
        background_tasks.add_task(
            send_order_notification_email,
            tenant,
            order
        )
    
    if tenant.whatsapp_notifications and tenant.notification_whatsapp:
        background_tasks.add_task(
            send_order_notification_whatsapp,
            tenant,
            order
        )
    
    # Track Facebook Pixel event
    if tenant.enable_facebook_pixel and tenant.facebook_access_token and order_data.fb_pixel_id:
        background_tasks.add_task(
            track_facebook_pixel_purchase,
            tenant,
            order,
            order_data.fb_event_id
        )
    
    return order


async def send_order_notification_email(tenant: Tenant, order: Order):
    """Send email notification to store owner"""
    email_service = EmailService()
    
    subject = "নতুন অর্ডার এসেছে"  # New order received
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>নতুন অর্ডার এসেছে</h2>
        <p>আপনার স্টোরে একটি নতুন অর্ডার এসেছে।</p>
        <p><strong>অর্ডার নম্বর:</strong> {order.order_number}</p>
        <p><strong>গ্রাহকের নাম:</strong> {order.customer_name}</p>
        <p><strong>মোবাইল নম্বর:</strong> {order.customer_phone}</p>
        <p><strong>ঠিকানা:</strong> {order.customer_address}</p>
        <p><strong>মোট পরিমাণ:</strong> {order.total} {tenant.currency}</p>
    </body>
    </html>
    """
    
    await email_service.send_email(
        tenant.notification_email,
        subject,
        html_body
    )


async def send_order_notification_whatsapp(tenant: Tenant, order: Order):
    """Send WhatsApp notification to store owner"""
    whatsapp_service = WhatsAppService()
    
    message = f"""নতুন অর্ডার এসেছে

অর্ডার নম্বর: {order.order_number}
গ্রাহকের নাম: {order.customer_name}
মোবাইল: {order.customer_phone}
ঠিকানা: {order.customer_address}
মোট: {order.total} {tenant.currency}"""
    
    await whatsapp_service.send_message(
        tenant.notification_whatsapp,
        message
    )


async def track_facebook_pixel_purchase(tenant: Tenant, order: Order, event_id: str):
    """Track purchase event via Facebook Pixel"""
    pixel_service = FacebookPixelService()
    
    # Get product IDs from order items
    content_ids = [str(item.product_id) for item in order.items]
    
    event_data = {
        "event_time": int(order.created_at.timestamp()),
        "event_id": event_id or f"order_{order.id}",
        "event_source_url": f"https://{tenant.slug}.{tenant.slug}/order/{order.id}",
        "user_data": {
            "phone": order.customer_phone,
            "email": order.customer_email
        },
        "custom_data": {
            "value": float(order.total),
            "currency": tenant.currency,
            "content_ids": content_ids,
            "num_items": sum(item.quantity for item in order.items)
        }
    }
    
    await pixel_service.track_purchase(
        tenant.facebook_pixel_id,
        tenant.facebook_access_token,
        event_data
    )


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    status_filter: Optional[OrderStatus] = None,
    limit: int = 50,
    offset: int = 0
):
    """List orders for tenant (owner only)"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    query = select(Order).where(Order.tenant_id == tenant.id)
    
    if status_filter:
        query = query.where(Order.status == status_filter)
    
    query = query.order_by(desc(Order.created_at)).limit(limit).offset(offset)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # Load items for each order
    for order in orders:
        items_result = await db.execute(
            select(OrderItem).where(OrderItem.order_id == order.id)
        )
        order.items = items_result.scalars().all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get order by ID"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    result = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.tenant_id == tenant.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Load items
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()
    
    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update order status"""
    tenant = get_tenant_from_request(request)
    
    if not tenant or tenant.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    result = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.tenant_id == tenant.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Update fields
    update_data = order_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    
    await db.commit()
    await db.refresh(order)
    
    # Load items
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()
    
    return order

