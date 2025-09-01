from app.models.order import Order,Cart ,OrderItem
from app.models.products import Product
from app.models.user import User
from app.schemas.order import OrderCreateSchema,OrderSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException,status
import uuid
from typing import List
from decimal import Decimal



class OrderService:
    
    async def get_orders(self, user_id:uuid.UUID , session:AsyncSession)-> List[Order]:
        satement = select(Order).where(Order.user_id == user_id).options(selectinload(Order.order_item).selectinload(OrderItem.product).selectinload(Product.product_gallery))
        result = await session.execute(satement)
        orders = result.scalars().all()
        return orders
    
    async def create_order(self, user_id:uuid.UUID , order_data:OrderCreateSchema, session:AsyncSession)-> Order:
        cart_item = await session.execute(
            select(Cart).where(Cart.user_id == user_id, Cart.is_ordered == False).options(selectinload(Cart.product))
        )
        cart_items = cart_item.scalars().all()
        # Check if cart is empty
        if not cart_items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No items in cart to create an order.")
         
        for item in cart_items:
            if item.product is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with ID {item.product_id} not found.")
            
            else:
                # Create Order
                order = Order(
                    user_id = user_id,
                    total_amount = item.quantity* Decimal(item.product.price),
                    payment_method = order_data.payment_method,
                    status = order_data.status
                    
                )
                
                session.add(order)
                await session.commit()
                await session.refresh(order)

                # Create  order items 
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    
                )
                session.add(order_item)
                await session.commit()  
                await session.refresh(order_item)
                # Mark cart item as 
                cart_delete = delete(Cart).where(Cart.id == item.id)
                await session.execute(cart_delete)
                await session.commit()
                await session.refresh(order_item)
        created_order = await self.get_order_by_id(order.id, session)
        return created_order

    async def get_order_by_id(self,order_id:uuid.UUID, session:AsyncSession)-> Order:
       statement =  select(Order).where(Order.id == order_id).options(selectinload(Order.order_item).selectinload(OrderItem.product).selectinload(Product.product_gallery))
       result = await session.execute(statement)
       return result.scalars().unique().one_or_none()
     
         