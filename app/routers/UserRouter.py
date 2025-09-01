from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.config.database import get_db
from app.services.user_services import UserService
from app.schemas.Users import UserCreateSchema, UserReadSchema 
from fastapi.security import OAuth2PasswordRequestForm
from  app.schemas.jwt_token import TokenSchema
from  app.schemas.base import SuccessResponse
from  app.utils.jwt_auth import verify_token
from typing import List
import uuid
from app.schemas.Users import LoginSchema

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]

)

user_service = UserService()


# For opeapi documentation
@router.post("/auth_login", response_model=SuccessResponse[TokenSchema])
async def oatuh2_login(
    fromdata: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    tokens = await user_service.login_user(session, fromdata.username, fromdata.password)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials", "errors": {"credentials": "Username or password is incorrect"}},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return SuccessResponse(
        message="Login successful",
        data=tokens,
        status=True
    )
    




    
# Login ROuter
@router.post("/login", response_model=SuccessResponse[TokenSchema])
async def login(login_data:LoginSchema, session: AsyncSession = Depends(get_db)):
    tokens = await user_service.login_user(session, login_data.model_dump())
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials", "errors": {"credentials": "Username or password is incorrect"}},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return SuccessResponse(
        message="Login successful",
        data=tokens,
        status=True)


# get current user  
@router.get("/", response_model=SuccessResponse[UserReadSchema])
async def get_current_user(session: AsyncSession = Depends(get_db) , current_user = Depends(verify_token)):
    user_id = current_user.get("userid")
    user = await user_service.get_current_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found", "errors": {"user_id": "No user with this ID"}}
        )
    return SuccessResponse(
        message="User retrieved successfully",
        data=user
    )
    

@router.get("/profile")
async def get_user_profile( session: AsyncSession = Depends(get_db),user=Depends(verify_token),):
    print("user from token",user)
    user_profile = await user_service.get_user_priofile(session, user.get("userid"))
    
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User profile not found", "errors": {"user_id": "No profile for this user ID"}}
        )
    
    return user_profile

# User Registration
@router.post("/register", response_model=SuccessResponse[UserReadSchema], status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)):
        new_user = await user_service.create_user(session, user_data)

        return SuccessResponse(
            message="User created successfully",
            data=new_user,
            status = True
        )


# Get all users 
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
    
    
# User  Delete 
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
    
    




    print("user from token",user)
    try:
        user_uuid = uuid.UUID(user["userid"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID in token"
        )
    
    user_profile = await user_service.get_user_priofile(session, user_uuid)
    
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User profile not found", "errors": {"user_id": "No profile for this user ID"}}
        )
    
    return user_profile