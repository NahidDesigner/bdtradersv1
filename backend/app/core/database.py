from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from sqlalchemy.pool import NullPool
from app.core.config import settings

# Convert postgresql:// to postgresql+asyncpg:// for async support
# Handle both postgresql:// and postgresql+asyncpg:// formats
if settings.DATABASE_URL.startswith("postgresql://"):
    database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif not settings.DATABASE_URL.startswith("postgresql+asyncpg://"):
    # If it's already async or some other format, use as-is
    database_url = settings.DATABASE_URL
else:
    database_url = settings.DATABASE_URL

engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    poolclass=NullPool if settings.ENVIRONMENT == "test" else None,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

