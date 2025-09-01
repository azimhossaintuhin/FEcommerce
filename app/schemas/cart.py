from  pydantic import BaseModel,Field,field_serializer
import uuid
from typing import List,Optional
from datetime import datetime
from  app.schemas.products import ProductSchema

class CartSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    created_at: datetime
    product: ProductSchema
    
    class Config:
        from_attributes = True
        
class CartCreateSchema(BaseModel):
    product_id: uuid.UUID
    quantity: int
    
    class Config:
        from_attributes = True