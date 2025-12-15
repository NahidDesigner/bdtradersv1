from pydantic_settings import BaseSettings
from typing import List, Union
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/bdtenant"
    
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
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Process CORS_ORIGINS - handle both string and list formats
if isinstance(settings.CORS_ORIGINS, str):
    if settings.CORS_ORIGINS == "*":
        settings.CORS_ORIGINS = ["*"]
    else:
        settings.CORS_ORIGINS = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

