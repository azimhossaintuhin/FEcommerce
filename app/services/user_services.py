from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User,UserProfile
from app.schemas.Users import UserCreateSchema,LoginSchema
from app.utils.jwt_auth import create_token_pair 
from app.schemas.jwt_token import TokenDataSchema
import uuid




class UserService:
    async def get_current_user(self, session: AsyncSession, user_id: int):
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().one_or_none()
        return user
    
    
    async def get_user_by_id(self, session: AsyncSession, user_id: int):
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().one_or_none()
        return user
    
    async def create_user(self, session: AsyncSession, user_data: UserCreateSchema):
        new_user = User(
            **user_data.model_dump()
        )
        new_user.set_password(user_data.password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
    
    async def delete_user(self, session: AsyncSession, user_id: int):
        quyery = await self.get_user_by_id(session, user_id)
        if quyery:
            await session.delete(quyery)
            await session.commit()
            return True
        return False
    
    async def get_user_priofile(self, session: AsyncSession, user_id):
        print("user id",user_id)
        user = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await session.execute(user)
        user_profile = result.scalars().one_or_none()
        print("user profile",user_profile)
        return user_profile
    
    async def login_user(self, session: AsyncSession, login_data:dict):
        username = login_data.get("username")
        password = login_data.get("password")
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().one_or_none()
        if user and user.check_password(password):
            token_data = TokenDataSchema(
                userid=str(user.id),
                username=user.username
            )
            tokens = create_token_pair(token_data,)
            return tokens
        return None

    
    
