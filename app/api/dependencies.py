
from typing import Annotated

from fastapi import BackgroundTasks, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme, oauth2_scheme_delivery_partner
from app.database.models import Seller, DeliveryPartner
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.product import ProductService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.services.shipment_event import ShipmentEventService
from app.services.delivery_partner import DeliveryPartnerService
from app.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

async def get_seller_service(session: SessionDep, tasks: BackgroundTasks):
    return SellerService(session, tasks)

async def get_product_service(session: SessionDep):
    return ProductService(session)

async def get_delivery_partner_service(session: SessionDep, tasks: BackgroundTasks):
    return DeliveryPartnerService(session, tasks)

async def get_shipment_event_service(session: SessionDep, tasks: BackgroundTasks):
    return ShipmentEventService(session, tasks)
# access token dependency for shipment and seller services
async def get_access_token_dependency(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> dict:
    data = decode_access_token(token)
    if data is None or await is_jti_blacklisted(data.get("jti", "")):
        raise HTTPException(status_code=401, detail="Invalid token")
    return data

# access token dependency for delivery partner
async def get_access_token_dependency_delivery_partner(token: Annotated[str, Depends(oauth2_scheme_delivery_partner)], session: SessionDep) -> dict:
    data = decode_access_token(token)
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(status_code=401, detail="Invalid token")
    return data

# logged in user dependency for shipment service
async def get_current_seller(token_data: Annotated[dict, Depends(get_access_token_dependency)], session: SessionDep) -> dict:
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))
    if seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller

# logged in delivery partner dependency
async def get_current_delivery_partner(token_data: Annotated[dict, Depends(get_access_token_dependency_delivery_partner)], session: SessionDep) -> DeliveryPartner:
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))
    if partner is None:
        raise HTTPException(status_code=404, detail="Delivery partner not found")
    return partner

# seller dep
sellerdep = Annotated[Seller, Depends(get_current_seller)]

# delivery partner dep
deliveryPartnerdep = Annotated[DeliveryPartner, Depends(get_current_delivery_partner)]


shipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)] 

sellerServiceDep = Annotated[SellerService, Depends(get_seller_service)] 

productServiceDep = Annotated[ProductService, Depends(get_product_service)]

deliveryPartnerServiceDep = Annotated[DeliveryPartnerService, Depends(get_delivery_partner_service)]

shipmentEventServiceDep = Annotated[ShipmentEventService, Depends(get_shipment_event_service)]

sessionDep = SessionDep