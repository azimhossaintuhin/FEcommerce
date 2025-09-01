from  app.schemas.products import ProductCreateSchema, CategoryINSchema, CategoryOutSchema
from  app.schemas.base import SuccessResponse, ErrorResponse
from  app.models import Product, Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , insert, update, delete
import uuid
from typing import List, Optional
from sqlalchemy.orm import selectinload

class CategroyService:
    
    async def  create_category(self,category_data: CategoryINSchema, session: AsyncSession):
        category = Category(
            **category_data.model_dump()
        )
        category.set_slug(category_data.name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    
    async def get_all_categories(self, session: AsyncSession) -> List[CategoryOutSchema]:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        return categories
    
    async def get_category_by_id(self, category_id: uuid.UUID, session: AsyncSession) -> Optional[CategoryOutSchema]:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalars().one_or_none()
        return category

    async  def update_category(self, category_id: uuid.UUID, category_data: CategoryINSchema, session: AsyncSession) -> Optional[CategoryOutSchema]:
        category = await self.get_category_by_id(category_id, session)
        if not category:
            return None
        for key, value in category_data.model_dump().items():
            setattr(category, key, value)
            category.set_slug(category_data.name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    
    async def delete_category(self, category_id: uuid.UUID, session: AsyncSession) -> bool:
        category = await self.get_category_by_id(category_id, session)
        if not category:
            return False
        await session.delete(category)
        await session.commit()
        return True
    
    async def products_by_category(self, category_id: uuid.UUID, session: AsyncSession):
        statement = (
            select(Product)
            .options(
                selectinload(Product.product_gallery),
                selectinload(Product.category)
            )
            .where(Product.category_id == category_id)
        )

        result = await session.execute(statement)  # <-- await here
        products = result.scalars().all()          # get list of Product objects
        return products
    