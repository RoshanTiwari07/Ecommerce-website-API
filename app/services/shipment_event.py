from app.database.models import ShipmentEvent, shipment, shipmentstatus, Seller
from app.services.base import BaseService
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import HTTPException, status

from app.services.notification import notificationservice


class ShipmentEventService(BaseService):
    def __init__(self, session: AsyncSession, tasks ):
        super().__init__(ShipmentEvent, session)
        self.notification_service = notificationservice(tasks)

    async def _verify_shipment_ownership(self, shipment_id: UUID, seller: Seller):
        """Verify that a seller owns a shipment"""
        shipment_obj = await self.session.get(shipment, shipment_id)
        if not shipment_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        if shipment_obj.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this shipment"
            )
        return shipment_obj

    async def add(
            self, 
            shipment_obj: shipment,
            location: str | None = None,
            status: shipmentstatus | None = None,
            zip_code: int | None = None
    ) -> ShipmentEvent:
        # If status or zip_code not provided, use the last event's values
        if not zip_code or not status:
            last_event = await self.get_latest_event(shipment_obj)
            if last_event:
                zip_code = zip_code or last_event.zip_code
                status = status or last_event.status
            else:
                # Fallback values if no previous event
                zip_code = zip_code or 0
                status = status or shipmentstatus.placed
        
        new_event = ShipmentEvent(
            shipment_id=shipment_obj.id,
            timestamp=datetime.now(),
            location=location,
            zip_code=zip_code,
            status=status
        )
        await self._notify(new_event, status)
        return await self._add(new_event)
    
    async def get_latest_event(self, shipment_obj: shipment) -> ShipmentEvent | None:
        """Get the latest event from a shipment's timeline"""
        if not shipment_obj.timeline or len(shipment_obj.timeline) == 0:
            return None
        
        timeline = sorted(shipment_obj.timeline, key=lambda event: event.created_at)
        return timeline[-1]
    
    async def get_events_by_shipment(self, shipment_id) -> list[ShipmentEvent]:
        """Get all events for a specific shipment"""
        from sqlalchemy import select
        query = select(ShipmentEvent).where(ShipmentEvent.shipment_id == shipment_id).order_by(ShipmentEvent.created_at)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def generate_description(self, event: ShipmentEvent) -> str:
        """Generate human-readable description for a shipment event"""
        match event.status:
            case shipmentstatus.placed:
                return "Your order has been placed successfully."
            case shipmentstatus.processing:
                return "Your order is being processed."
            case shipmentstatus.shipped:
                return f"Your order has been shipped from {event.location}."
            case shipmentstatus.in_transit:
                return f"Your order is currently in transit and passing through {event.location}."
            case shipmentstatus.out_for_delivery:
                return f"Your order is out for delivery and will arrive soon at {event.location}."
            case shipmentstatus.delivered:
                return f"Your order has been delivered to {event.location}."
            case _:
                return "Your order status has been updated."
    
    async def create_event_for_shipment(
        self,
        shipment_id: UUID,
        seller: Seller,
        location: str | None = None,
        event_status: shipmentstatus | None = None,
        zip_code: int | None = None
    ) -> ShipmentEvent:
        """Create a shipment event with authorization check"""
        shipment_obj = await self._verify_shipment_ownership(shipment_id, seller)
        return await self.add(shipment_obj, location, event_status, zip_code)
    
    async def get_shipment_events_for_seller(
        self,
        shipment_id: UUID,
        seller: Seller
    ) -> list[ShipmentEvent]:
        """Get all events for a shipment with authorization check"""
        await self._verify_shipment_ownership(shipment_id, seller)
        return await self.get_events_by_shipment(shipment_id)
    
    async def get_latest_event_for_seller(
        self,
        shipment_id: UUID,
        seller: Seller
    ) -> ShipmentEvent:
        """Get latest event for a shipment with authorization check"""
        shipment_obj = await self._verify_shipment_ownership(shipment_id, seller)
        latest_event = await self.get_latest_event(shipment_obj)
        
        if not latest_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No events found for this shipment"
            )
        
        return latest_event
    
    async def _notify(self, event: ShipmentEvent, status: shipmentstatus):
        match status:
            case shipmentstatus.placed:
                await self.notification_service.send_email(
                    recipients=[event.shipment.client_contact_email],
                    subject="Shipment Placed",
                    body=f"Your shipment {event.shipment.name} has been placed successfully."
                        f"The estimated delivery date is {event.shipment.estimated_delivery}."
                        f"The shipment will be deliverd by {event.shipment.delivery_partner.name}."
                )
            case shipmentstatus.out_for_delivery:
                await self.notification_service.send_email(
                    recipients=[event.shipment.client_contact_email],
                    subject="Shipment Out for Delivery",
                    body=f"Your shipment {event.shipment.name} is out for delivery and will arrive soon at {event.location}"
                )