from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.schemas.auth import OTPRequest, OTPVerify, PasswordLogin, TokenResponse, UserCreate, UserResponse
from app.models.user import User
from app.services.otp import OTPService
import random
import string

router = APIRouter()


@router.post("/otp/request", response_model=dict)
async def request_otp(
    request: OTPRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request OTP for phone number login"""
    # Generate 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    
    # Store OTP (in production, use Redis with expiration)
    # For now, we'll use a simple in-memory store or database
    # TODO: Implement Redis-based OTP storage
    
    # Send OTP via SMS service
    otp_service = OTPService()
    await otp_service.send_otp(request.phone, otp)
    
    # In development, return OTP for testing
    # Remove this in production!
    if True:  # Set to False in production
        return {
            "message": "OTP sent successfully",
            "otp": otp  # Remove in production
        }
    
    return {"message": "OTP sent successfully"}


@router.post("/otp/verify", response_model=TokenResponse)
async def verify_otp(
    request: OTPVerify,
    db: AsyncSession = Depends(get_db)
):
    """Verify OTP and login/register user"""
    # Verify OTP (in production, check against Redis)
    # For now, accept any 6-digit code in development
    # TODO: Implement proper OTP verification
    
    # Check if user exists
    result = await db.execute(
        select(User).where(User.phone == request.phone)
    )
    user = result.scalar_one_or_none()
    
    # Create user if doesn't exist
    if not user:
        user = User(
            phone=request.phone,
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.uuid), "user_id": user.id}
    )
    
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "uuid": str(user.uuid),
            "phone": user.phone,
            "email": user.email,
            "full_name": user.full_name
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: PasswordLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with phone/email and password"""
    # Find user by phone or email
    if request.phone:
        result = await db.execute(
            select(User).where(User.phone == request.phone)
        )
    elif request.email:
        result = await db.execute(
            select(User).where(User.email == request.email)
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone or email is required"
        )
    
    user = result.scalar_one_or_none()
    
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.uuid), "user_id": user.id}
    )
    
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "uuid": str(user.uuid),
            "phone": user.phone,
            "email": user.email,
            "full_name": user.full_name
        }
    )


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register new user"""
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.phone == user_data.phone)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this phone number already exists"
        )
    
    # Create new user
    user = User(
        phone=user_data.phone,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password) if user_data.password else None,
        is_active=True
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.uuid), "user_id": user.id}
    )
    
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "uuid": str(user.uuid),
            "phone": user.phone,
            "email": user.email,
            "full_name": user.full_name
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(lambda: None),  # Will be extracted from header in dependency
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user"""
    # TODO: Implement proper JWT dependency
    # For now, this is a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet"
    )

