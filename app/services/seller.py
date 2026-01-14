
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from app.services.user import UserService


class SellerService(UserService):
    def __init__(self, session: AsyncSession, tasks: BackgroundTasks):
        super().__init__(Seller, session, tasks)

    async def add(self, credentials: SellerCreate) -> Seller:
        return await self._add_user(credentials.model_dump()
                                    , "seller")
    
    async def token(self, email: str, password: str) -> str:
        return await self.generate_token(email, password)
    
    
