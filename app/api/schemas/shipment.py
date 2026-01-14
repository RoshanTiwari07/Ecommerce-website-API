from dataclasses import field
from http import client
from pydantic import BaseModel, Field
from datetime import datetime

from uuid import UUID
from app.database.models import Seller, shipmentstatus



class base_shipment(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    destination: int = Field(
        description="Pincode of the destination location"
        )

class ProductInShipment(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)

class shipment_get(base_shipment):
    id: UUID
    seller: Seller
    status: shipmentstatus
    estimated_delivery: datetime | None = None
    products: list["ProductInShipment"] = []
    delivery_partner_id: UUID | None = None
    created_at: datetime

class create_shipment(base_shipment):
    products: list[ProductInShipment]
    status: shipmentstatus = shipmentstatus.placed
    client_contact_email: str | None = None
    client_contact_phone: int | None = field(default=None)
    
class shipment_update(BaseModel):
    status: shipmentstatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)


# Shipment Event Schemas
class create_shipment_event(BaseModel):
    location: str | None = None
    status: shipmentstatus
    zip_code: int | None = None


class shipment_event_response(BaseModel):
    id: UUID
    shipment_id: UUID
    timestamp: datetime
    location: str | None = None
    zip_code: int | None = None
    status: shipmentstatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class shipment_event_with_description(shipment_event_response):
    description: str