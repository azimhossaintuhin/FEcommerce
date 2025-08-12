from  sqlalchemy.ext.asyncio import AsyncSession
from  app.models.base import User
from  app.schemas.user_schema import UserIn
from sqlalchemy import select

class UserServices:
    async def create_user(self, data: UserIn, session: AsyncSession):
            query =  await session.execute(
            select(User).where(User.email == data.email)
        )
            if not query.scalar_one_or_none():
                user = User(
                    email=data.email,
                    is_superuser=data.is_superuser,
                    is_staff=data.is_staff,
                    is_verified=data.is_verified
                )
                user.save_password(data.password)
                session.add(user)
                await session.commit()
                await  session.refresh(user)
                print(f"User created: {user.__dict__.items()}")
                return {key: values for key, values in user.__dict__.items() if not key.startswith('_') and key != 'password' }
            raise ValueError("User with this email already exists")
        

    async def get_user(self, user_id: str, session: AsyncSession):
        try:  
            user =  await session.execute(select(User).where(User.id == user_id))
            if user :
                return {key:value for key, value in  user.scalar_one().__dict__.items() if not key.startswith('_') and key != 'password'}
            raise ValueError("User not found")
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None 
    
    async def get_users(self,session:AsyncSession):
        try:
            users = await session.execute(select(User).order_by(User.email))

            return users.scalars().all()

        except Exception as e:
            print(f"Error fetching users: {e}")
            return []