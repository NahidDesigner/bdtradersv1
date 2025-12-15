from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.middleware.tenant import TenantMiddleware
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Cleanup if needed
    pass


app = FastAPI(
    title="BD Tenant SaaS Platform",
    description="Multi-tenant SaaS platform for Bangladesh merchants",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (for subdomain security)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure based on your domain
)

# Tenant Middleware (must be after CORS)
app.add_middleware(TenantMiddleware)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "BD Tenant SaaS Platform API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Coolify and load balancers"""
    return {"status": "healthy", "service": "bd-tenant-backend"}


@app.get("/api/v1/health")
async def api_health_check():
    """API health check endpoint"""
    return {"status": "healthy", "service": "bd-tenant-backend"}

