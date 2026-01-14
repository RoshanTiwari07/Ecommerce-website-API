import asyncio

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.config import notification_settings

# Filter out non-ConnectionConfig fields
mail_config_data = notification_settings.model_dump()
# Remove fields that ConnectionConfig doesn't accept
mail_config_data.pop('USER_CREDENTIALS', None)
mail_config_data.pop('VALIDATE_CREDENTIALS', None)

fastmail = FastMail(
    ConnectionConfig(
        **mail_config_data,
    )
)

async def send_message():
    await fastmail.send_message(
        message= MessageSchema(
            recipients=["roshan9tiwari@gmail.com"],
            subject="Test Email from FastShip",
            body="This is a test email sent from FastShip application.",
            subtype=MessageType.plain
        )
    )
    print("Email sent successfully")

asyncio.run(send_message())