from  fastapi import APIRouter, Depends, HTTPException, status
from  typing import List
from  app.schemas.products import ProductCreateSchema,ProductSchema,CategoryINSchema,CategoryOutSchema
from  app.schemas.base import SuccessResponse, ErrorResponse
from  app.services.productServices import ProductService
from  sqlalchemy.ext.asyncio import AsyncSession
from  app.config.database import get_db as get_session
from  app.utils.jwt_auth import verify_token
import uuid

router = APIRouter(
    prefix="/api/v1",
    tags=["Products"]
)

product_service = ProductService()



# +++++++++++++  Categeory Realated  Routes ++++++++++++++
@router.post("/categories", response_model=SuccessResponse[CategoryOutSchema])
async def create_category(category_data: CategoryINSchema,session: AsyncSession = Depends(get_session),current_user=Depends(verify_token)):
    try:
        category = await product_service.create_category(category_data, session)
        
        return SuccessResponse(
            message="Category created successfully",
            data=category,
            status=True
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to create category",
            errors={"exception": str(e)},
            status=False
        )

@router.get("/categories", response_model=SuccessResponse[List[CategoryOutSchema]])
async def get_all_categories(session: AsyncSession = Depends(get_session)):
    categories = await product_service.get_all_categories(session)
    return SuccessResponse(
        message="Categories fetched successfully",
        data=categories,
        status=True
    )
    
@router.get("/categories/{category_id}", response_model=SuccessResponse[CategoryOutSchema])
async def get_category_by_id(category_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    category = await product_service.get_category_by_id(category_id, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return SuccessResponse(
        message="Category fetched successfully",
        data=category,
        status=True
    )


@router.patch("/categories/{category_id}", response_model=SuccessResponse[CategoryOutSchema])
async def update_category(category_id: uuid.UUID, category_data: CategoryINSchema, session: AsyncSession = Depends(get_session), current_user=Depends(verify_token)):
    try:
        updated_category = await product_service.update_category(category_id, category_data, session)
        return SuccessResponse(
            message="Category updated successfully",
            data=updated_category,
            status=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update category: {str(e)}",
        )

@router.delete("/categories/{category_id}", response_model=SuccessResponse[bool])
async def delete_category(category_id: uuid.UUID, session: AsyncSession = Depends(get_session), current_user=Depends(verify_token)):
    category = await product_service.get_category_by_id(category_id, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    success = await product_service.delete_category(category_id, session)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete category"
        )
    return SuccessResponse(
        message="Category deleted successfully",
        data=True,
        status=True
    )

        
        
