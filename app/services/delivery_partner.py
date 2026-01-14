from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.api.schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerUpdate
from app.database.models import DeliveryPartner, shipment, shipmentstatus
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession, tasks: BackgroundTasks):
        super().__init__(DeliveryPartner, session, tasks)

    async def signup(self, credentials: DeliveryPartnerCreate) -> DeliveryPartner:
        return await self._add_user(credentials.model_dump()
                                    , "delivery_partner")
    
    async def token(self, email: str, password: str) -> str:
        return await self.generate_token(email, password)
    
    async def get_by_id(self, partner_id: UUID) -> DeliveryPartner:
        """Get delivery partner by ID"""
        partner = await self.session.get(DeliveryPartner, partner_id)
        
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery partner not found"
            )
        
        return partner
    
    async def get_assigned_shipments(self, partner_id: UUID) -> list[shipment]:
        """Get all shipments assigned to this delivery partner"""
        result = await self.session.execute(
            select(shipment).where(shipment.delivery_partner_id == partner_id)
        )
        return result.scalars().all()
    
    async def get_shipments_by_zip(self, partner_id: UUID, zip_code: int) -> list[shipment]:
        """Get shipments in a specific zip code area for the partner"""
        result = await self.session.execute(
            select(shipment).where(
                shipment.delivery_partner_id == partner_id,
                shipment.destination == zip_code
            )
        )
        return result.scalars().all()
    
    async def update_shipment_status(
        self, 
        partner_id: UUID, 
        shipment_id: UUID, 
        new_status: shipmentstatus
    ) -> shipment:
        """Update the status of a shipment"""
        shipment_obj = await self.session.get(shipment, shipment_id)
        
        if not shipment_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        # Verify the shipment is assigned to this partner
        if shipment_obj.delivery_partner_id != partner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this shipment"
            )
        
        shipment_obj.status = new_status
        self.session.add(shipment_obj)
        await self.session.commit()
        await self.session.refresh(shipment_obj)
        return shipment_obj
    
    async def update_profile(
        self, 
        partner_id: UUID, 
        update_data: DeliveryPartnerUpdate
    ) -> DeliveryPartner:
        """Update delivery partner profile"""
        partner = await self.get_by_id(partner_id)
        
        partner.sqlmodel_update(update_data.model_dump(exclude_unset=True))
        self.session.add(partner)
        await self.session.commit()
        await self.session.refresh(partner)
        return partner
