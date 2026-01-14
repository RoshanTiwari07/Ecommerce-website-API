from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID

class BaseProduct(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category: str | None = None

class ProductCreate(BaseProduct, ):
    price: float = Field(gt=0, description="Price must be greater than zero")
    stock_quantity: int = Field(ge=0, description="Stock quantity cannot be negative")

class SellerBasicInfo(BaseModel):
    id: UUID
    name: str
    email: EmailStr

class ProductRead(BaseProduct):
    id: UUID
    seller_id: UUID
    seller: SellerBasicInfo
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    name: str | None = None        
    description: str | None = None    
    price: float | None = None        
    stock_quantity: int | None = None 
    category: str | None = None  
