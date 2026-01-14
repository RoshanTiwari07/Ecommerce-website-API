
from fastapi import APIRouter, status
from ..dependencies import sellerdep, shipmentEventServiceDep
from uuid import UUID
from ..schemas.shipment import (
    create_shipment_event,
    shipment_event_response,
    shipment_event_with_description
)

router = APIRouter(prefix="/shipment-events", tags=["shipment-events"])


@router.post("/{shipment_id}", response_model=shipment_event_response)
async def create_shipment_event(
    shipment_id: UUID,
    event_data: create_shipment_event,
    service: shipmentEventServiceDep,
    seller: sellerdep
):
    """Create a new shipment event"""
    new_event = await service.create_event_for_shipment(
        shipment_id=shipment_id,
        seller=seller,
        location=event_data.location,
        event_status=event_data.status,
        zip_code=event_data.zip_code
    )
    return new_event


@router.get("/{shipment_id}", response_model=list[shipment_event_response])
async def get_shipment_events(
    shipment_id: UUID,
    service: shipmentEventServiceDep,
    seller: sellerdep
):
    """Get all events for a shipment"""
    events = await service.get_shipment_events_for_seller(shipment_id, seller)
    return events


@router.get("/{shipment_id}/latest", response_model=shipment_event_with_description)
async def get_latest_shipment_event(
    shipment_id: UUID,
    service: shipmentEventServiceDep,
    seller: sellerdep
):
    """Get the latest event for a shipment with description"""
    latest_event = await service.get_latest_event_for_seller(shipment_id, seller)
    description = await service.generate_description(latest_event)
    
    return {
        **latest_event.__dict__,
        "description": description
    }
