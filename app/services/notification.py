from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from app.config import notification_settings


mail_config_data = notification_settings.model_dump()
# Remove fields that ConnectionConfig doesn't accept
mail_config_data.pop('USER_CREDENTIALS', None)
mail_config_data.pop('VALIDATE_CREDENTIALS', None)


class notificationservice:
    def __init__(self, task: BackgroundTasks):
        self.fastmail = FastMail(
            ConnectionConfig(
               **mail_config_data,
        )
    )
    async def send_email(self, subject: str, recipients: list[EmailStr], body: str):
        self.tasks.add_task(
            self.fastmail.send_message,
            message= MessageSchema(
                    recipients=recipients,
                    subject=subject,
                    body=body,
                    subtype=MessageType.plain
                ) 
            )