from fastapi import APIRouter
from  app.schemas.user_schema import UserIn,UserOut
from app.schemas.Base import SuccessResponse,ErrorResponse
from  app.services.user_services import UserServices
from app.config.database import Session

router = APIRouter(prefix="/auth")
user_service = UserServices()

@router.get("/user/{user_id}" ,response_model=SuccessResponse)
async def get_user(user_id: str , session: Session):
    user =  await user_service.get_user(user_id, session)
    if user:
        return SuccessResponse(message="User found", data=user)
    return SuccessResponse(message="User not found", data={})


@router.get("/users", response_model=SuccessResponse)
async def get_users(session: Session):
    query = await user_service.get_users(session)
    if query:
        return {"message": "Users fetched successfully", "data": [UserOut.model_validate(user) for user in query]}
    return {"message": "No users found", "data": []}    

@router.post("/user")
async def create_user(user: UserIn, session: Session):
        new_user = await user_service.create_user(user, session)
        if new_user:
            return SuccessResponse(
                message="User created successfully",
                data=new_user
            )