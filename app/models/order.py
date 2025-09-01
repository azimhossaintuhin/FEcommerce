from  .base import BaseModel ,Order_payment_Type,Order_status_Type
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float,DECIMAL,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime ,timezone
from .products import Product
from .user import User
from  typing import List



class Cart(BaseModel):
    __tablename__ = "carts"
    user_id =  Column(UUID(as_uuid=True),ForeignKey('users.id' , ondelete='CASCADE'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id' , ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    is_ordered = Column(Boolean, default=False)
    user = relationship("User", backref="carts",uselist=True)
    product = relationship("Product", backref="carts",uselist=False)
    
    def __str__(self):
        return f"Cart(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})"
    
    def get_total_price(self):
        return self.quantity * self.product.price if self.product else 0.0
    
    
class Order(BaseModel):
      __tablename__ = "orders"
      order_id = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4().hex[:4].upper()))
      user_id = Column(UUID(as_uuid=True), ForeignKey("users.id" , ondelete='CASCADE'), nullable=False)
      total_amount = Column(DECIMAL(10, 2), nullable=False)
      payment_method = Column(Enum(Order_payment_Type), nullable=False, default=Order_payment_Type.COD)
      status = Column(Enum(Order_status_Type), nullable=False, default=Order_status_Type.PENDING)
      user = relationship("User", backref="orders")
      order_item = relationship("OrderItem", backref="orders", uselist=True)

    



class OrderItem(BaseModel):
    __tablename__ = "order_items"
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id" , ondelete='CASCADE'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id" , ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    order = relationship("Order", backref="order_items")
    product = relationship("Product", backref="order_items")
    
    
    def __str__(self):
        return f"OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})"
    
      