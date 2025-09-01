from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy import select
from  sqlalchemy.orm import selectinload
from app.models import Product,ProductGallery
from app.schemas.products import ProductCreateSchema, ProductSchema, ProductGalleryOutSchema,ProductGalleryInSchema
import uuid
from  app.utils.file_handler import save_upload_file
from typing import List

class ProductService:
    
    async def get_all_products(self,session:AsyncSession)->list[ProductSchema]:
        statement =  select(Product).options(
            selectinload(Product.product_gallery),
            selectinload(Product.category)
        )
        result = await session.execute(statement)
        return result.scalars().all()
    
    
    async def get_product_by_id(self,product_id:uuid.UUID,session:AsyncSession)->ProductSchema|None:
        statement =  select(Product).options(
            selectinload(Product.product_gallery),
            selectinload(Product.category)
        ).where(Product.id==product_id)
        result = await session.execute(statement)
        return result.scalars().one_or_none()
    
    
    async def create_product(self, product_data: ProductCreateSchema, session: AsyncSession):
        # Create product
        product = Product(
            **product_data.model_dump(exclude={"image", "product_gallery"})
        )
        product.set_slug(product_data.name)
        product.image = save_upload_file(product_data.image) if product_data.image else None
        session.add(product)
        await session.commit()
        await session.refresh(product)

        # Add product gallery
        if product_data.product_gallery:
            for file in product_data.product_gallery:
                image_path = save_upload_file(file, "product_gallery")
                gallery = ProductGallery(
                    product_id=product.id,
                    image_url=image_path
                )
                session.add(gallery)
            await session.flush()
            await session.commit()

        # Reload product with relationships
        result = await session.execute(
            select(Product)
            .options(
                selectinload(Product.product_gallery),
                selectinload(Product.category)
            )
            .where(Product.id == product.id)
        )

        product_obj = result.scalars().one_or_none()  # only call once
        return product_obj
    
    
    
    async def update_product(self, product_id: uuid.UUID, product_data: ProductCreateSchema, session: AsyncSession):
        reasult = await  session.execute(select(Product).where(Product.id==product_id))
        product = reasult.scalars().one_or_none()
        if not product:
            return None
        for key,value in product_data.model_dump(exclude={"image","product_gallery"}).items():
            setattr(product,key,value)
            if  product_data.image:
                product.image = save_upload_file(product_data.image)
        await session.commit()
        await session.refresh(product)
        return product
    
    
    async def delete_product(self, product_id: uuid.UUID, session: AsyncSession):
        statement = await  session.execute(select(Product).where(Product.id==product_id))
        product = statement.scalars().one_or_none()
        if not product:
            return False
        await session.delete(product)
        await session.commit()
        return True
    
    
    async def update_gallery_by_id(self,gallery_id:int,gallery_data:ProductGalleryInSchema.as_form,session:AsyncSession)->ProductGalleryOutSchema|None:
        statement =  select(ProductGallery).where(ProductGallery.id==gallery_id)
        result = await session.execute(statement)
        gallery_item = result.scalars().one_or_none()
        if not gallery_item:
            return None
        gallery_item.image_url = save_upload_file(gallery_data,"product_gallery")
        await session.commit()
        await session.refresh(gallery_item)
        return gallery_item
    
    async def update_product_gallery(self,product_id:uuid.UUID,files:List[UploadFile],session:AsyncSession)->List[ProductGalleryOutSchema]|None:
        statement =  select(Product).where(Product.id==product_id)
        result = await session.execute(statement)
        product = result.scalars().one_or_none()
        if not product:
            return None
        gallery_items = []
        for file in files:
            image_path = save_upload_file(file, "product_gallery")
            gallery = ProductGallery(
                product_id=product.id,
                image_url=image_path
            )
            session.add(gallery)
            gallery_items.append(gallery)
        await session.flush()
        await session.commit()
        return gallery_items

    def delete_product_gallery(self,gallery_id:int,session:AsyncSession)->bool:
        statement =  session.execute(select(ProductGallery).where(ProductGallery.id==gallery_id))
        gallery_item = statement.scalars().one_or_none()
        if not gallery_item:
            return False
        session.delete(gallery_item)
        session.commit()
        return True
    

