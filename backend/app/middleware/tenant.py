from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.models.tenant import Tenant
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
import re


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Multi-tenant middleware that extracts tenant from subdomain.
    
    Example:
    - app.mysaas.com -> main app (no tenant)
    - storename.mysaas.com -> tenant: storename
    """
    
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "")
        
        # Extract subdomain from host
        # Format: subdomain.domain.com or subdomain.domain.com:port
        host_parts = host.split(":")
        hostname = host_parts[0]
        
        # Skip tenant resolution for:
        # - API health checks
        # - Static files
        # - Main app domain (no subdomain)
        if (
            request.url.path.startswith("/health") or
            request.url.path.startswith("/static") or
            request.url.path.startswith("/api/v1/health")
        ):
            return await call_next(request)
        
        # Extract subdomain
        parts = hostname.split(".")
        tenant_slug = None
        
        # If we have more than 2 parts, assume first is subdomain
        # e.g., storename.mysaas.com -> storename
        if len(parts) >= 3:
            tenant_slug = parts[0]
            # Skip common subdomains that aren't tenants
            if tenant_slug in ["www", "api", "app", "admin"]:
                tenant_slug = None
        
        # Resolve tenant from database
        tenant = None
        if tenant_slug:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(Tenant).where(
                        Tenant.slug == tenant_slug,
                        Tenant.is_active == True
                    )
                )
                tenant = result.scalar_one_or_none()
                
                if not tenant:
                    # Tenant not found - return 404 for store pages
                    if not request.url.path.startswith("/api"):
                        from fastapi.responses import JSONResponse
                        return JSONResponse(
                            status_code=404,
                            content={"detail": "Store not found"}
                        )
        
        # Store tenant in request state
        request.state.tenant = tenant
        request.state.tenant_slug = tenant_slug
        
        response = await call_next(request)
        return response

