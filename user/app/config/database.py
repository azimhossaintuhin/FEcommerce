from  sqlalchemy.ext.asyncio import AsyncSession ,create_async_engine,async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from  typing import AsyncGenerator ,  Annotated
from fastapi import Depends
from  decouple import config

DATABASE_URL = f'postgresql+asyncpg://{config("DATABASE_URL")}'
BASE = declarative_base()
async_engine = create_async_engine(DATABASE_URL,echo=True, future=True)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)



async def get_session()->AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
    await session.commit()
    await session.close()
    
Session = Annotated[AsyncSession, Depends(get_session)]