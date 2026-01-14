from sqlmodel import Column, Relationship, SQLModel, Field
from enum import Enum
from datetime import datetime
from pydantic import EmailStr
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER
from app.database.types import shipmentstatus_enum

class shipmentstatus(str, Enum):
    placed = "placed"
    processing = "processing"
    shipped = "shipped"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class ShipmentProduct(SQLModel, table=True):
    """Association table for many-to-many relationship between Shipment and Product"""
    __tablename__ = "shipment_product"
    
    shipment_id: UUID = Field(foreign_key="shipment.id", primary_key=True)
    product_id: UUID = Field(foreign_key="product.id", primary_key=True)
    quantity: int = Field(default=1)  # Quantity of this product in the shipment
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class shipment(SQLModel, table=True):
    __tablename__ = "shipment"
    id: UUID | None = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    name: str = Field()
    description: str
    price: float
    status: shipmentstatus = Field(sa_column=Column(shipmentstatus_enum, nullable=False))
    destination: int
    estimated_delivery: datetime
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    client_contact_email: EmailStr | None = None    
    client_contact_phone: int | None = None

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"})
    delivery_partner_id: UUID | None = Field(foreign_key="delivery_partner.id")
    delivery_partner: "DeliveryPartner" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"})
    
    # Many-to-many relationship with products
    products: list["Product"] = Relationship(back_populates="shipments", link_model=ShipmentProduct)
    
    # Timeline of shipment events
    timeline: list["ShipmentEvent"] = Relationship(back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"})

class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"
    id: UUID | None = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    ) 
    shipment_id: UUID = Field(foreign_key="shipment.id")
    timestamp: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    location: str | None = None
    zip_code: int | None = None
    status: shipmentstatus = Field(sa_column=Column(shipmentstatus_enum, nullable=False), default=shipmentstatus.placed)

    shipment: "shipment" = Relationship(back_populates="timeline", sa_relationship_kwargs={"lazy": "selectin"})


class User(SQLModel):
        name: str
        email: EmailStr
        email_verified: bool = Field(default=False)
        password_hash: str


class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID | None = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    address: str
    zip_code: int
    # relationship to shipments
    shipments: list[shipment] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"})
    products: list["Product"] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"})



class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: UUID | None = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    name: str
    description: str
    price: float
    seller_id: UUID = Field(foreign_key="seller.id")
    stock_quantity: int
    category: str
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    seller: "Seller" = Relationship(sa_relationship_kwargs={"lazy": "selectin"}, back_populates="products")
    # Many-to-many relationship with shipments
    shipments: list["shipment"] = Relationship(back_populates="products", link_model=ShipmentProduct)

class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID | None = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    zip_code: list[int] = Field(sa_column=Column(ARRAY(INTEGER)))
    max_handling_capacity: int

    shipments: list[shipment] = Relationship(back_populates="delivery_partner", sa_relationship_kwargs={"lazy": "selectin"})