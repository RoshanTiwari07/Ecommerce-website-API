from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from app.database.redis import add_jti_to_blacklist


from ..dependencies import get_access_token_dependency, sellerServiceDep
from ..schemas.seller import SellerCreate, SellerRead

# from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/seller", tags=["seller"])

@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: sellerServiceDep):
    return await service.add(seller)

@router.get("/verify")
async def verify_seller_email(token: str, service: sellerServiceDep):
    service.verify_email(token)
    return {"msg": "Email verified successfully"}

# login for seller can be added here
@router.post("/token")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: sellerServiceDep):
        token = await service.token(request_form.username, request_form.password)
        return {"access_token": token, "token_type": "bearer"}

# logout 
@router.post("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_access_token_dependency)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"msg": "Successfully logged out"}


