from  app.schemas.cart import CartCreateSchema, CartSchema
from  app.schemas.base import SuccessResponse, ErrorResponse
from app.services.cart_services import CartService
from  app.config.database import get_db
from  fastapi import APIRouter, Depends, HTTPException, status
from  app.utils.jwt_auth import verify_token
from  typing import List
import uuid


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"]
)
cart_services = CartService()



# +++++++++++++  Cart Realated  Routes ++++++++++++++
@router.get("/", response_model=SuccessResponse[List[CartSchema]])
async def  get_all_cart_items(session=Depends(get_db), current_user=Depends(verify_token)):
    try:
        user_id = current_user.get("userid")
        cart_items =  await cart_services.get_cart_by_user(user_id, session)
        return SuccessResponse(
            message="Cart items fetched successfully",
            data=cart_items,
            status=True
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to fetch cart items",
            errors={"exception": str(e)},
            status=False
        )


@router.post("/", response_model=SuccessResponse[CartSchema])
async def add_to_cart(cart_data: CartCreateSchema, session=Depends(get_db), current_user=Depends(verify_token)):
        user_id = current_user.get("userid")
        cart_item = await cart_services.add_to_cart(cart_data, user_id, session)
        cart = await cart_services.get_cart_by_id(cart_item.id, session)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart item not found")

        return SuccessResponse(
        message="Item added to cart successfully",
        data=cart,  # CartSchema will read ORM object with from_attributes
        status=True
    )
        


@router.patch("/{cart_id}", response_model=SuccessResponse[CartSchema])
async def update_cart_item(cart_id: uuid.UUID, quantity: int, session=Depends(get_db), current_user=Depends(verify_token)):
    try:
        user_id = current_user.get("userid")
        if  cart_services.get_cart_by_id(cart_id, session) is None:
            raise HTTPException(status_code=404, detail="Cart item not found")
        cart = await cart_services.update_cart_item(cart_id, user_id, quantity, session)

        return SuccessResponse(
            message="Cart item updated successfully",
            data=cart,
            status=True
        )
    except Exception as e:
     print(e)


@router.delete("/{cart_id}", response_model=SuccessResponse[None])
async def remove_cart_item(cart_id: uuid.UUID, session=Depends(get_db), current_user=Depends(verify_token)):
    try:
        user_id = current_user.get("userid")
        await cart_services.remove_from_cart(cart_id, user_id, session)
        return SuccessResponse(
            message="Cart item removed successfully",
            data=None,
            status=True
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to remove cart item",
            errors={"exception": str(e)},
            status=False
        )

@router.delete("/clear", response_model=SuccessResponse[None])
async def clear_cart(session=Depends(get_db), current_user=Depends(verify_token)):
    try:
        user_id = current_user.get("userid")
        await cart_services.clear_cart(user_id, session)
        return SuccessResponse(
            message="Cart cleared successfully",
            data=None,
            status=True
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to clear cart",
            errors={"exception": str(e)},
            status=False
        )