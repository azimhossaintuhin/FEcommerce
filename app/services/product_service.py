from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy import select
from  sqlalchemy.orm import selectinload
from app.models import Product,ProductGallery
from app.schemas.products import ProductCreateSchema, ProductSchema, ProductGalleryOutSchema

from  app.utils.file_handler import save_upload_file


class ProductService:
    
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