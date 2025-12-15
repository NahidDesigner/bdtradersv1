from fastapi import APIRouter
from app.api.v1 import auth, tenants, products, orders, shipping, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(shipping.router, prefix="/shipping", tags=["Shipping"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

