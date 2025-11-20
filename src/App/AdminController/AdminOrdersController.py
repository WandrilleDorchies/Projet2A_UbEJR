from fastapi import APIRouter, Depends, HTTPException, status

from src.App.init_app import order_service
from src.App.JWTBearer import AdminBearer

admin_orders_router = APIRouter(prefix="", tags=["Orders"], dependencies=[Depends(AdminBearer())])


# ORDERS
@admin_orders_router.get(
    "/orders", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_orders(limit: int = 15):
    try:
        if limit < 0:
            raise HTTPException(
                status_code=403, detail="You should choose a positive number of orders to see."
            )
        return order_service.get_all_orders(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}") from e


@admin_orders_router.get(
    "/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_order_by(order_id: int):
    try:
        order = order_service.get_order_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail=f"Order with id [{order_id}] not found")
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@admin_orders_router.put(
    "/orders/{order_id}/prepared",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def mark_order_as_prepared(order_id: int):
    try:
        updated_order = order_service.mark_as_prepared(order_id)
        return updated_order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
