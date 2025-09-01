from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from  app.services.product_service import ProductService
from  app.schemas.products import ProductCreateSchema, ProductSchema,ProductGalleryInSchema, ProductGalleryOutSchema
from  app.schemas.base import SuccessResponse, ErrorResponse
from typing import List
import uuid

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"]
)

product_service = ProductService()




# Get All Products
@router.get("/", response_model=SuccessResponse[List[ProductSchema]])
async def get_all_products(session: AsyncSession = Depends(get_db)):
    try:
        products = await product_service.get_all_products(session)
        return SuccessResponse(
            message="Products fetched successfully",
            data=products,
            status=True
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to fetch products",
            errors={"detail": str(e)},
            status=False
        )

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

# Get Product by ID
@router.get("/{product_id}", response_model=SuccessResponse[ProductSchema])
async def get_product_by_id(product_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    product = await product_service.get_product_by_id(product_id, session)
    if product:
        return SuccessResponse(
            message="Product fetched successfully",
            data=product,
            status=True
        )
    return ErrorResponse(
        message="Product not found",
        errors={"product_id": "No product found with the given ID"},
        status=False
    )

# Update Product by ID  
@router.put("/{product_id}", response_model=SuccessResponse[ProductSchema])
async def update_product_by_id(
    product_id: uuid.UUID,
    product_data: ProductCreateSchema = Depends(ProductCreateSchema.as_form),
    session: AsyncSession = Depends(get_db)
):
    product = await product_service.update_product(product_id, product_data, session)
    if product:
        return SuccessResponse(
            message="Product updated successfully",
            data=product,
            status=True
        )
    return ErrorResponse(
        message="Product not found",
        errors={"product_id": "No product found with the given ID"},
        status=False
    )
    
# Delete Product by ID
@router.delete("/{product_id}", response_model=SuccessResponse[None])
async def delete_product_by_id(product_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    product = await product_service.get_product_by_id(product_id, session)
    if product:
        await session.delete(product)
        await session.commit()
        return SuccessResponse(
            message="Product deleted successfully",
            data=None,
            status=True
        )
    return ErrorResponse(
        message="Product not found",
        errors={"product_id": "No product found with the given ID"},
        status=False
    )
    

router.put("/gallery/{product_id}", response_model=SuccessResponse[List[ProductGalleryOutSchema]])
async def update_product_gallery(
    product_id: uuid.UUID,
    files: List[ProductGalleryInSchema] = Depends(ProductGalleryInSchema.as_form),
    session: AsyncSession = Depends(get_db)
):
    gallery_items = await product_service.update_product_gallery(product_id, files, session)
    if gallery_items is not None:
        return SuccessResponse(
            message="Product gallery updated successfully",
            data=gallery_items,
            status=True
        )
    return ErrorResponse(
        message="Product not found",
        errors={"product_id": "No product found with the given ID"},
        status=False
    )
