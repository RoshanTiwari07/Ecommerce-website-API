from fastapi import APIRouter, HTTPException
from ..schemas.product import ProductCreate, ProductRead, ProductUpdate
# from app.database.models import Product
from ..dependencies import productServiceDep, sellerdep
from uuid import UUID


router = APIRouter(prefix="/product", tags=["product"])

@router.get("/", response_model=list[ProductRead])
async def get_all_products(
    service: productServiceDep,
    skip: int = 0,
    limit: int = 100
):
    """Get all products with pagination"""
    return await service.get_all_products(skip, limit)

@router.get("/{id}")
async def get_product(
    id: UUID, 
    service: productServiceDep):
    product = await service.get_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
    

@router.post("/", response_model=ProductRead)
async def create_product(
    seller: sellerdep, 
    service:productServiceDep, 
    body: ProductCreate):
    return await service.create_product(seller.id, body)

@router.get("/seller/{seller_id}/products", response_model=list[ProductRead])
async def get_products_by_seller(
    seller_id: UUID,
    service: productServiceDep):
    return await service.get_by_seller(seller_id)

@router.put("/{id}", response_model=ProductRead)
async def update_product(
    id: UUID,
    body: ProductUpdate,
    service: productServiceDep,
    seller: sellerdep
    ):
    product = await service.get_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.seller_id != seller.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    return await service.update_product(id, body)

@router.delete("/{id}")
async def delete_product(
    id: UUID,
    service: productServiceDep,
    seller: sellerdep
    ):
    product = await service.get_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.seller_id != seller.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    await service.delete_product(id)
    return {"detail": "Product deleted successfully"}


@router.get("/{id}/stock")
async def check_product_stock(
    id: UUID,
    service: productServiceDep
):
    """Check stock availability for a product"""
    return await service.check_stock(id)