
from typing import Any

from fastapi import APIRouter, HTTPException, status
from ..dependencies import shipmentServiceDep, sellerdep
from app.database.models import shipment, shipmentstatus
from uuid import UUID
from ..schemas.shipment import create_shipment, shipment_update

router = APIRouter(prefix="/shipment", tags=["shipment"])


@router.get("/", response_model=shipment)
# call the function and taking id and session as parameters :- id is integer and sessionDep is used to call and get the session
async def get_shipment(id: UUID, service: shipmentServiceDep):
    # Get shipment from database and creating an object of shipment
    shipment_obj = await service.get(id)
    
    if shipment_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    # return the shipment object as a response as the output of the function is a shipment data model
    return shipment_obj

@router.post("/", response_model=shipment)
# create a function to submit shipment taking body which has what input is required and session as parameters and output is a dictionary meaning the params are key value pairs
async def submit_shipment(body: create_shipment, service: shipmentServiceDep, seller: sellerdep) -> shipment:
    # create a new shipment object using the data from the request body
    return await service.create(seller.id, body)


@router.get("/{field}")
async def get_shipment_field(field: str, id: UUID, service: shipmentServiceDep) -> Any:
    shipment_obj = await service.get(id)
    if shipment_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return getattr(shipment_obj, field)


@router.patch("/", response_model=shipment_update)
async def patch_shipment(id: UUID, body: shipment_update, service: shipmentServiceDep):

    update = body.model_dump(exclude_unset=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    shipment = await service.update(id, body)
    return shipment


@router.delete("/")
async def delete_shipment(id: UUID, service: shipmentServiceDep) -> dict[str, str | int | Any]:
    await service.delete(id)
    return {"detail": "Shipment deleted successfully"}


@router.get("/status/{status}", response_model=list[shipment])
async def get_shipments_by_status(status: shipmentstatus, service: shipmentServiceDep):
    """Get all shipments with a specific status"""
    return await service.get_by_status(status)


@router.patch("/{id}/assign-partner", response_model=shipment)
async def assign_delivery_partner(
    id: UUID, 
    partner_id: UUID, 
    service: shipmentServiceDep,
    seller: sellerdep
):
    """Assign a delivery partner to a shipment"""
    shipment_obj = await service.get(id)
    
    if not shipment_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    # Verify the seller owns this shipment
    if shipment_obj.seller_id != seller.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this shipment"
        )
    
    return await service.assign_delivery_partner(id, partner_id)