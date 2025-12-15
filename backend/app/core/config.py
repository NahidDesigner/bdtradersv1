from pydantic_settings import BaseSettings
from typing import List, Union
import os


class Settings(BaseSettings):
    # Database - can be full URL or constructed from parts
    DATABASE_URL: str = ""
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "bdtenant"
    POSTGRES_HOST: str = "postgres"
    # POSTGRES_PORT can be empty string from env, so we handle it specially
    POSTGRES_PORT: str = "5432"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # CORS - Can be comma-separated string or list
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:5173,http://localhost:3000"
    
    # Domain
    BASE_DOMAIN: str = "localhost"
    ALLOWED_SUBDOMAINS: str = "*"
    
    # SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@bdtenant.com"
    SMTP_FROM_NAME: str = "BD Tenant Platform"
    
    # WhatsApp
    WHATSAPP_API_KEY: str = ""
    WHATSAPP_API_URL: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    
    # OTP
    OTP_PROVIDER: str = "local"
    OTP_API_KEY: str = ""
    OTP_API_URL: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Upload
    MAX_UPLOAD_SIZE: str = "10485760"  # 10MB - handle as string, convert later
    UPLOAD_DIR: str = "uploads"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: str = "false"  # Handle as string, convert to bool later
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Convert string values to proper types
settings.POSTGRES_PORT = int(settings.POSTGRES_PORT) if settings.POSTGRES_PORT and settings.POSTGRES_PORT.strip() else 5432
settings.JWT_EXPIRATION_HOURS = int(settings.JWT_EXPIRATION_HOURS) if settings.JWT_EXPIRATION_HOURS and settings.JWT_EXPIRATION_HOURS.strip() else 24
settings.MAX_UPLOAD_SIZE = int(settings.MAX_UPLOAD_SIZE) if settings.MAX_UPLOAD_SIZE and settings.MAX_UPLOAD_SIZE.strip() else 10485760
settings.DEBUG = settings.DEBUG.lower() in ("true", "1", "yes") if isinstance(settings.DEBUG, str) else bool(settings.DEBUG)
settings.SMTP_PORT = int(settings.SMTP_PORT) if settings.SMTP_PORT and str(settings.SMTP_PORT).strip() else 587

# Construct DATABASE_URL if not provided
if not settings.DATABASE_URL:
    settings.DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Process CORS_ORIGINS - handle both string and list formats
if isinstance(settings.CORS_ORIGINS, str):
    if settings.CORS_ORIGINS == "*":
        settings.CORS_ORIGINS = ["*"]
    else:
        settings.CORS_ORIGINS = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
