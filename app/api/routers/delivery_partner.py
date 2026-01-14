from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from uuid import UUID

from ..schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerRead, DeliveryPartnerUpdate
from app.database.models import shipment, shipmentstatus
from ..dependencies import deliveryPartnerServiceDep, deliveryPartnerdep, get_access_token_dependency_delivery_partner
from app.database.redis import add_jti_to_blacklist

router = APIRouter(prefix="/delivery-partner", tags=["delivery-partner"])


@router.post("/signup", response_model=DeliveryPartnerRead, status_code=status.HTTP_201_CREATED)
async def register_delivery_partner(
    partner_data: DeliveryPartnerCreate, 
    service: deliveryPartnerServiceDep
):
    """Register a new delivery partner"""
    return await service.signup(partner_data)


@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()], 
    service: deliveryPartnerServiceDep
):
    """Login for delivery partner - returns JWT token"""
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/verify")
async def verify_delivery_partner_email(token: str, service: deliveryPartnerServiceDep):
    await service.verify_email(token)
    return {"msg": "Email verified successfully"}


@router.post("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_access_token_dependency_delivery_partner)]
):
    """Logout delivery partner by blacklisting the token"""
    await add_jti_to_blacklist(token_data["jti"])
    return {"msg": "Successfully logged out"}


@router.get("/shipments", response_model=list[shipment])
async def get_assigned_shipments(
    partner: deliveryPartnerdep,
    service: deliveryPartnerServiceDep
):
    """Get all shipments assigned to this delivery partner"""
    return await service.get_assigned_shipments(partner.id)


@router.get("/shipments/zip/{zip_code}", response_model=list[shipment])
async def get_shipments_by_zip(
    partner: deliveryPartnerdep,
    zip_code: int,
    service: deliveryPartnerServiceDep
):
    """Get shipments in a specific zip code area for the partner"""
    return await service.get_shipments_by_zip(partner.id, zip_code)


@router.patch("/shipments/{shipment_id}/status", response_model=shipment)
async def update_shipment_status(
    partner: deliveryPartnerdep,
    shipment_id: UUID,
    new_status: shipmentstatus,
    service: deliveryPartnerServiceDep
):
    """Update the delivery status of a shipment"""
    return await service.update_shipment_status(partner.id, shipment_id, new_status)


@router.get("/me", response_model=DeliveryPartnerRead)
async def get_current_partner_profile(partner: deliveryPartnerdep):
    """Get current authenticated delivery partner details"""
    return partner


@router.patch("/me", response_model=DeliveryPartnerRead)
async def update_current_partner_profile(
    partner: deliveryPartnerdep,
    update_data: DeliveryPartnerUpdate,
    service: deliveryPartnerServiceDep
):
    """Update current delivery partner profile (zip codes, capacity)"""
    return await service.update_profile(partner.id, update_data)
