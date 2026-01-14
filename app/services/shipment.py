from datetime import datetime, timedelta
import re
from uuid import UUID
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.database.models import shipment, shipmentstatus, Product, ShipmentProduct
from app.api.schemas.shipment import create_shipment, shipment_update

class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession):
        # providing the model to the base service as well as the session for DB operations
        super().__init__(shipment, session)

    async def get(self, id: UUID) -> shipment | None:
        return await self._get(id)

    async def _validate_product_availability(self, product_items: list) -> None:
        """Validate that all products exist and have sufficient stock."""
        for product_item in product_items:
            product = await self.session.get(Product, product_item.product_id)
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {product_item.product_id} not found"
                )
            
            if product.stock_quantity < product_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product.name}. Available: {product.stock_quantity}, Requested: {product_item.quantity}"
                )

    async def _create_shipment_products(self, shipment_id: UUID, product_items: list) -> None:
        """Create shipment-product relationships and deduct stock."""
        for product_item in product_items:
            # Create ShipmentProduct entry
            shipment_product = ShipmentProduct(
                shipment_id=shipment_id,
                product_id=product_item.product_id,
                quantity=product_item.quantity
            )
            self.session.add(shipment_product)
            
            # Deduct stock
            product = await self.session.get(Product, product_item.product_id)
            product.stock_quantity -= product_item.quantity

    async def create(self, seller_id: UUID, shipment_create: create_shipment) -> shipment:
        """Create a new shipment with products."""
        # 1. Validate all products exist and have sufficient stock
        await self._validate_product_availability(shipment_create.products)
        
        # 2. Create shipment
        new_shipment = shipment(
            **shipment_create.model_dump(exclude={'products', 'status'}),
            seller_id=seller_id,
            status=shipmentstatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3)
        )
        
        self.session.add(new_shipment)
        await self.session.flush()  # Get the shipment ID without committing
        
        # 3. Create shipment-product relationships and update stock
        await self._create_shipment_products(new_shipment.id, shipment_create.products)
        
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment
        

    async def update(self, id: UUID, shipment_upd: shipment_update) -> shipment:
        update_shipment = await self.session.get(shipment, id)
        
        if not update_shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        update_shipment.sqlmodel_update(shipment_upd.model_dump(exclude_unset=True))
        return await self._update(update_shipment)

    async def delete(self, id: UUID) -> None:
        shipment_to_delete = await self.get(id)
        
        if not shipment_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        await self._delete(shipment_to_delete)
    
    async def assign_delivery_partner(self, shipment_id: UUID, partner_id: UUID) -> shipment:
        shipment_obj = await self.get(shipment_id)
        
        if not shipment_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        shipment_obj.delivery_partner_id = partner_id
        return await self._add(shipment_obj)
    
    async def get_by_status(self, status: shipmentstatus) -> list[shipment]:
        result = await self.session.execute(
            select(shipment).where(shipment.status == status)
        )
        return result.scalars().all()