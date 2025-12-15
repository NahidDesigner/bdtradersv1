from app.core.config import settings
import httpx
import logging
import uuid

logger = logging.getLogger(__name__)


class FacebookPixelService:
    """Service for Facebook Pixel and Meta Conversion API events"""
    
    async def track_purchase(
        self,
        pixel_id: str,
        access_token: str,
        event_data: dict
    ):
        """
        Track purchase event via Meta Conversion API
        
        event_data should contain:
        - event_name: "Purchase"
        - event_id: unique event ID for deduplication
        - user_data: phone, email, etc.
        - custom_data: value, currency, content_ids, etc.
        """
        try:
            if not access_token or not pixel_id:
                return False
            
            # Generate event ID if not provided
            event_id = event_data.get("event_id") or str(uuid.uuid4())
            
            payload = {
                "data": [{
                    "event_name": "Purchase",
                    "event_time": event_data.get("event_time"),
                    "event_id": event_id,
                    "event_source_url": event_data.get("event_source_url"),
                    "action_source": "website",
                    "user_data": {
                        "ph": event_data.get("user_data", {}).get("phone"),
                        "em": event_data.get("user_data", {}).get("email"),
                    },
                    "custom_data": {
                        "value": event_data.get("custom_data", {}).get("value"),
                        "currency": event_data.get("custom_data", {}).get("currency", "BDT"),
                        "content_ids": event_data.get("custom_data", {}).get("content_ids", []),
                        "content_type": "product",
                        "num_items": event_data.get("custom_data", {}).get("num_items", 1),
                    }
                }]
            }
            
            # Send to Meta Conversion API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://graph.facebook.com/v18.0/{pixel_id}/events",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"Facebook Pixel event tracked: {result}")
                return True
        except Exception as e:
            logger.error(f"Failed to track Facebook Pixel event: {e}")
            return False

