from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from  app.services.product_service import ProductService
from  app.schemas.products import ProductCreateSchema, ProductSchema
from  app.schemas.base import SuccessResponse, ErrorResponse
from typing import List
import uuid

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"]
)

product_service = ProductService()



# Create Product
@router.post("/", response_model=SuccessResponse[ProductSchema])
async def create_product(
    product_data: ProductCreateSchema = Depends(ProductCreateSchema.as_form),
    session: AsyncSession = Depends(get_db)
):
    product = await product_service.create_product(product_data, session)
    return SuccessResponse(
        message="Product created successfully",
        data=product,
        status=True
    )