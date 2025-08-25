from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import declarative_base
from  decouple import config
BASE = declarative_base()


DATABASE_URL = config("DATABASE_URL", default="sqlite+aiosqlite:///./test.db")


engine = create_async_engine(DATABASE_URL, echo=True)

sessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with sessionLocal() as session:
        yield session
        