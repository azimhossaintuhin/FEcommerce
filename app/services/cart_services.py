
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from  app.models.order import Cart
from  app.schemas.cart import CartCreateSchema, CartSchema
from  sqlalchemy.orm import selectinload
from app.models.products import Product
import uuid

class CartService:
    
    async def add_to_cart(self, cart_data: CartCreateSchema,user_id:uuid.UUID, session:AsyncSession ):  
        statemet = Cart(
            **cart_data.model_dump(),
            user_id=user_id
        )
        print("cart item to be added",statemet)
        session.add(statemet)
        await session.commit()
        await session.refresh(statemet)
        return statemet
    
    
    async def get_cart_by_id(self, cart_id: uuid.UUID, session: AsyncSession) -> CartSchema | None:
        statement = select(Cart).where(Cart.id == cart_id).options(
            selectinload(Cart.product).selectinload(Product.product_gallery)
        )
        result = await session.execute(statement)
        cart = result.scalars().one_or_none()
        return cart  # Pydantic can now read this because relationships are loaded
    
    async def get_cart_by_user(self,user_id:uuid.UUID, session:AsyncSession) -> list[Cart]:
        statement = select(Cart).where(Cart.user_id==user_id).options(
            selectinload(Cart.product).selectinload(Product.product_gallery)
        )
        result = await session.execute(statement)
        return result.scalars().all()
    

    async def update_cart_item(self, cart_id:uuid.UUID, user_id:uuid.UUID, quantity:int, session:AsyncSession) -> None:
        statement = update(Cart).where(Cart.id==cart_id, Cart.user_id==user_id).values(quantity=quantity)
        await session.execute(statement)
        await session.commit()
        return await self.get_cart_by_id(cart_id, session)
    
    async def remove_from_cart(self, cart_id:uuid.UUID, user_id:uuid.UUID, session:AsyncSession) -> None:
        statement = delete(Cart).where(Cart.id==cart_id, Cart.user_id==user_id)
        await session.execute(statement)
        await session.commit()
        return None
        
        
    async def clear_cart(self, user_id:uuid.UUID, session:AsyncSession) -> None:
        statement = delete(Cart).where(Cart.user_id==user_id)
        await session.execute(statement)
        await session.commit()
        return None
    
    