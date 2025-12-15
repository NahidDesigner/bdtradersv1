from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import engine, Base
from app.middleware.tenant import TenantMiddleware
from app.api.v1 import api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    # Log connection info (without password) for debugging
    db_url_safe = settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "***"
    logger.info(f"Connecting to database at: ***@{db_url_safe}")
    logger.info(f"Database user: {settings.POSTGRES_USER}, host: {settings.POSTGRES_HOST}, port: {settings.POSTGRES_PORT}, db: {settings.POSTGRES_DB}")
    
    # Retry connection with exponential backoff
    import asyncio
    max_retries = 10
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database connection successful! Tables created/verified.")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, 10)  # Exponential backoff, max 10s
            else:
                logger.error(f"Database connection failed after {max_retries} attempts: {str(e)}")
                logger.error("Please check:")
                logger.error("1. POSTGRES_HOST is set to 'postgres' (service name)")
                logger.error("2. POSTGRES_PASSWORD in backend service matches postgres service")
                logger.error("3. Postgres service is running and healthy")
                logger.error("4. If database already exists, password must match the original password")
                raise
    
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

