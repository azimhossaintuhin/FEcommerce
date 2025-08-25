from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert,update,delete,func
from app.models.User import User
from app.schemas.Users import UserCreateSchema, UserReadSchema



class UserService:
    async def get_all_users(self, session: AsyncSession):
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
    
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
    
    
    
    