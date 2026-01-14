from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID


class DeliveryPartnerBase(BaseModel):
    name: str
    email: EmailStr


class DeliveryPartnerCreate(DeliveryPartnerBase):
    password: str = Field(min_length=8, description="Password must be at least 8 characters")
    zip_code: list[int] = Field(description="List of zip codes/pin codes the partner can deliver to")
    max_handling_capacity: int = Field(gt=0, description="Maximum number of shipments the partner can handle")


class DeliveryPartnerRead(DeliveryPartnerBase):
    id: UUID
    zip_code: list[int]
    max_handling_capacity: int
    created_at: datetime

    class Config:
        from_attributes = True


class DeliveryPartnerUpdate(BaseModel):
    zip_code: list[int] | None = None
    max_handling_capacity: int | None = Field(default=None, gt=0)
