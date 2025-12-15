from app.core.config import settings
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str = None
    ):
        """Send email via SMTP"""
        if not settings.SMTP_HOST:
            logger.warning("SMTP not configured, skipping email send")
            return False
        
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            message["To"] = to_email
            
            if text_body:
                message.attach(MIMEText(text_body, "plain"))
            message.attach(MIMEText(html_body, "html"))
            
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                use_tls=True,
            )
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def render_template(self, template_str: str, context: dict) -> str:
        """Render email template with context"""
        template = Template(template_str)
        return template.render(**context)

