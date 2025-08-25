from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.config.database import get_db
from app.services.userservices import UserService
from app.schemas.Users import UserCreateSchema, UserReadSchema 
from  app.schemas.base import SuccessResponse 
from typing import List
import uuid

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_service = UserService()



@router.get("/", response_model=SuccessResponse[List[UserReadSchema]])
async def get_all_users(session: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(session)
    if not users:
        return SuccessResponse(
            message="No users found",
            data=[],
            status=True
        )
    return SuccessResponse(
        message="Users retrieved successfully",
        data=users,
        status=True
    )
    


@router.post("/", response_model=SuccessResponse[UserReadSchema], status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)):
        new_user = await user_service.create_user(session, user_data)

        return SuccessResponse(
            message="User created successfully",
            data=new_user,
            status = True
        )
@router.get("/{user_id}", response_model=SuccessResponse[UserReadSchema])
async def get_user_by_id(user_id:uuid.UUID, session: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found", "errors": {"user_id": "No user with this ID"}}
        )
    return SuccessResponse(
        message="User retrieved successfully",
        data=user
    )
    
@router.delete("/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    success = await user_service.delete_user(session, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found", "errors": {"user_id": "No user with this ID"}}
        )
    return SuccessResponse(
        message="User deleted successfully",
        data={"user_id": user_id}
    )