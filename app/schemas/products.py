
from pydantic import Field,EmailStr,BaseModel,field_serializer
from fastapi import File, UploadFile,Form
from typing import Optional,List
import uuid
from datetime import datetime
from .base import BASE_URL



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


class ProductGalleryInSchema(BaseModel):
    product_id: uuid.UUID = Field(...)
    image_url: str = Field(..., max_length=255)
    
    class Config:
        from_attributes = True
        
    @classmethod
    def as_form(
        cls,
        product_id: uuid.UUID = Form(...),
        image_url: str = Form(..., max_length=255),
    ):
        return cls(
            product_id=product_id,
            image_url=image_url
        )
    
    
    
class ProductGalleryOutSchema(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    image_url: str = Field(..., max_length=255)
    class Config:
        from_attributes = True
        
    @field_serializer("image_url")
    def serialize_image_url(self, image_url: str) -> str:
        return f"{BASE_URL}/{image_url}" if image_url else None




class ProductCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    slug: Optional[str] = None
    image: UploadFile = File(None)
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: uuid.UUID = Field(...)
    is_published: bool = True
    product_gallery: Optional[List[UploadFile]] = None

    
    @classmethod
    def as_form(
        cls,
        name: str = Form(..., max_length=100),
        slug: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price: float = Form(...),
        stock: int = Form(0),
        category_id: uuid.UUID = Form(...),
        is_published: bool = Form(True),
        product_gallery: Optional[List[UploadFile]] = None,
        image: UploadFile = None,
    ):
        return cls(
            name=name,
            slug=slug,
            image=image,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            is_published=is_published,
            product_gallery=product_gallery 
        )



class ProductSchema(BaseModel):
    id: uuid.UUID 
    name: str = Field(..., max_length=100)
    slug: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: uuid.UUID = Field(...)
    product_gallery: Optional[List[ProductGalleryOutSchema]] = []
    is_published: bool = True

    class Config:
        from_attributes = True
        
    @field_serializer("image")
    def serialize_image(self, image: Optional[str]) -> Optional[str]:
        return f"{BASE_URL}/{image}" if image else None