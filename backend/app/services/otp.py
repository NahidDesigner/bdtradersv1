from app.core.config import settings
import httpx
import logging

logger = logging.getLogger(__name__)


class OTPService:
    """Service for sending OTP via SMS"""
    
    async def send_otp(self, phone: str, otp: str):
        """
        Send OTP to phone number.
        
        In production, integrate with SMS provider like:
        - Twilio
        - Nexmo/Vonage
        - Local Bangladesh SMS gateway
        """
        try:
            if settings.OTP_PROVIDER == "local":
                # For development/testing - just log
                logger.info(f"OTP for {phone}: {otp}")
                return True
            
            # Example integration with external API
            # async with httpx.AsyncClient() as client:
            #     response = await client.post(
            #         settings.OTP_API_URL,
            #         json={
            #             "phone": phone,
            #             "message": f"Your OTP is: {otp}",
            #             "api_key": settings.OTP_API_KEY
            #         }
            #     )
            #     response.raise_for_status()
            
            return True
        except Exception as e:
            logger.error(f"Failed to send OTP: {e}")
            raise

