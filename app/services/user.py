from uuid import UUID
from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import select
from app.services.base import BaseService
from app.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.services.notification import notificationservice
from app.utils import decode_url_token, generate_access_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService):
    def __init__(self, model: User ,session: AsyncSession, tasks: BackgroundTasks):
        self.model = model
        self.session = session
        self.notification_service = notificationservice(tasks)

    async def _add_user(self, data:dict, router_prefix: str) -> User:
        # Extract password before unpacking
        password = data.pop("password")
        user = self.model(
            **data,
            password_hash=password_context.hash(password)
        )
        user = await self._add(user)
        token = generate_access_token(data={
                "email": user.email,
                "id": str(user.id),
        })
        await self.notification_service.send_email(
            recipients=[user.email],
            subject="verify your email",
            context= {
                "name": user.name,
                "verification_url": f"http://localhost:8000/{router_prefix}/verify?token={token}"
            }
        )
        return user 
    
    async def verify_email(self, token: str) -> User:
        token_data = decode_url_token(token)
        if not token_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired token"
                )
        user = await self._get(UUID(token_data["id"]))
        user.email_verified = True
        self._update(user)

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
    
    if not User.email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified"
            )
        
    async def generate_token(self, email: str, password: str) -> str:
        user = await self.get_by_email(email)
        if user is None or not password_context.verify(
            password, 
            user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Email or password is incorrect"
            )
        return generate_access_token(data={
            "user": {
                "name": user.name,
                "id": str(user.id),
            }
        })