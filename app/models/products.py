from  sqlalchemy import Column, Integer, String, Float, Text,Boolean,ForeignKey,UUID
from sqlalchemy.orm import relationship
from .base import BaseModel

class Category(BaseModel):
        __tablename__ = 'categories'
        name = Column(String(100), nullable=False, unique=True)
        slug = Column(String(100), nullable=True, unique=True)
        products = relationship("Product", back_populates="category")
        
        def __str__(self):
            return self.name
        
        def  set_slug(self,slug):
            self.slug = self.name.replace(" ","-").lower()

        



class Product(BaseModel):
    __tablename__ = 'products'
    
    name = Column(String(100), nullable=False)
    slug =  Column(String(100), nullable=True, unique=True)
    image  =  Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id',ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products")
    is_published = Column(Boolean, default=True)
    product_gallery = relationship("ProductGallery", back_populates="product",)
    

    def __str__(self):
        return self.name    
    
    def set_slug(self,slug):
        self.slug = self.name.replace(" ","-").lower()
    
    
    

class ProductGallery(BaseModel):
    __tablename__ = 'product_galleries'
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id',ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    product = relationship("Product", backref="galleries")
    
    def __str__(self):
        return f"ProductGallery(id={self.id}, product_id={self.product_id}, image_url={self.image_url})"
    
    
    