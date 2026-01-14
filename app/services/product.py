from sqlmodel import select
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.product import ProductCreate, ProductUpdate
from app.database.models import Product


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, seller_id: UUID, body: ProductCreate)-> Product:
        # creating an instance of Product model so that a database entry can be made
        create = Product(
            **body.model_dump(),
            seller_id=seller_id
        )
        self.session.add(create)
        await self.session.commit()
        await self.session.refresh(create)
        return create


    async def get_product(self, id: UUID) -> Product:
        return await self.session.get(Product, id)

    async def get_by_seller(self, seller_id: UUID) -> list[Product]:
        result = await self.session.execute(
            select(Product).where(Product.seller_id == seller_id)
        )
        # return all products for the particular seller_id
        return result.scalars().all()

    async def update_product(self, product_id: UUID, body: ProductUpdate) -> Product:
        # here we get the product by its id and then update its details instead of creating a new entry
        update = await self.session.get(Product, product_id)
        update.sqlmodel_update(body.model_dump(exclude_unset=True))
        self.session.add(update)
        await self.session.commit()
        await self.session.refresh(update)
        return update

    async def delete_product(self, id: UUID) -> None:
        delete = await self.session.get(Product, id)
        await self.session.delete(delete)
        await self.session.commit()

    async def reduced_stock(self, product_id: UUID, quantity: int) -> Product:
        get_product = await self.session.get(Product, product_id)
        get_product.stock_quantity -= quantity
        if get_product.stock_quantity < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        self.session.add(get_product)
        await self.session.commit()
        await self.session.refresh(get_product)
        return get_product
    
    async def get_all_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """Get all products with pagination"""
        result = await self.session.execute(
            select(Product).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def check_stock(self, product_id: UUID) -> dict:
        """Check stock availability for a product"""
        product = await self.session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "product_id": product.id,
            "product_name": product.name,
            "stock_quantity": product.stock_quantity,
            "available": product.stock_quantity > 0
        }