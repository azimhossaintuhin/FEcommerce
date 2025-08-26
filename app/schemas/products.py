
from pydantic import Field,EmailStr,BaseModel
from typing import Optional
import uuid
from datetime import datetime



class CategoryINSchema(BaseModel):
    name: str = Field(..., max_length=100)
    slug: Optional[str] = None
    class Config:
        from_attributes = True

class CategoryOutSchema(BaseModel):
    id: uuid.UUID
    name: str
    slug: Optional[str] = None
    class Config:
        from_attributes = True


class ProductCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    slug: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: uuid.UUID = Field(...)
    is_published: bool = True

    class Config:
        from_attributes = True

class ProductSchema(BaseModel):
    name: str = Field(..., max_length=100)
    slug: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: CategoryOutSchema = Field(...)
    is_published: bool = True

    class Config:
        from_attributes = True
    