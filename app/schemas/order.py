from  pydantic import BaseModel,Field,field_serializer
import uuid
from typing import List,Optional
from datetime import datetime
from  app.schemas.products import ProductSchema
from  app.models.order import Order_payment_Type,Order_status_Type


class OrderItemSchema(BaseModel):
    product_id: uuid.UUID
    quantity: int
    product: ProductSchema
    class Config:
        from_attributes = True


class OrderCreateSchema(BaseModel):
    payment_method:Order_payment_Type
    status: Order_status_Type
    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id: uuid.UUID
    order_id: str
    user_id: uuid.UUID
    total_amount: float
    payment_method:Order_payment_Type
    status: Order_status_Type
    created_at: datetime
    updated_at: datetime
    order_item: Optional[List[OrderItemSchema]] = []
    
    class Config:
        from_attributes = True