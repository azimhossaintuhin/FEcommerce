from  app.services.order_services import OrderService
from  app.config.database import get_db
from  fastapi import APIRouter, Depends, HTTPException, status
from  app.schemas.order import OrderCreateSchema,OrderSchema
from  app.schemas.base import SuccessResponse, ErrorResponse
from  app.utils.jwt_auth import verify_token
import uuid


router = APIRouter(
    prefix="/api/v1/order",
    tags=["Order"]
)

order_services = OrderService()

# +++++++++++++  Order Realated  Routes ++++++++++++++
@router.get("/", response_model=SuccessResponse[list[OrderSchema]])
async def  get_all_orders(session=Depends(get_db), current_user=Depends(verify_token)):
    try:
        user_id = current_user.get("userid")
        orders =  await order_services.get_orders(user_id, session)
        return SuccessResponse(
            message="Orders fetched successfully",
            data=orders,
            status=True
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to fetch orders",
            errors={"exception": str(e)},
            status=False
        )

@router.post("/", response_model=SuccessResponse[OrderSchema])
async def create_order( order_data:OrderCreateSchema,session=Depends(get_db), current_user=Depends(verify_token)):
        try:
            user_id = current_user.get("userid")
            order = await order_services.create_order(user_id, order_data, session)
            return SuccessResponse(
                message="Order created successfully",
                data=order,
                status=True
            )
        except HTTPException as http_exc:
            raise http_exc



@router.get("/{order_id}", response_model=SuccessResponse[OrderSchema])
async def get_order_by_id(order_id: uuid.UUID, session=Depends(get_db), current_user=Depends(verify_token)):
    user_id = current_user.get("userid")
    order = await order_services.get_order_by_id(order_id, session)
    if not order or str(order.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or access denied"
        )
    return SuccessResponse(
        message="Order fetched successfully",
        data=order,
        status=True
    )