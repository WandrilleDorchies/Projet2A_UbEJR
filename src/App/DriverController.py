from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.Order import OrderState

from .init_app import customer_service, driver_service, gm_service, jwt_service, order_service
from .JWTBearer import DriverBearer

driver_router = APIRouter(
    prefix="/drivers", tags=["Drivers"], dependencies=[Depends(DriverBearer())]
)


def get_driver_id_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(DriverBearer())],
) -> int:
    token = credentials.credentials
    driver_id = int(jwt_service.validate_user_jwt(token)["user_id"])
    return driver_id


def get_current_order_id(driver_id: int = Depends(get_driver_id_from_token)) -> int:
    order = driver_service.get_driver_current_order(driver_id)
    return order.order_id


# PROFILE
@driver_router.get("/me", status_code=status.HTTP_200_OK, dependencies=[Depends(DriverBearer())])
def get_profile(driver_id: int = Depends(get_driver_id_from_token)):
    try:
        driver = driver_service.get_driver_by_id(driver_id)
        return driver
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {e}") from e


@driver_router.put("/me", status_code=status.HTTP_200_OK, dependencies=[Depends(DriverBearer())])
def update_profile(
    driver_first_name: str = None,
    driver_last_name: str = None,
    driver_phone: str = None,
    driver_id: int = Depends(get_driver_id_from_token),
):
    try:
        update_data = locals()
        update_data.pop("driver_id")
        updated_driver = driver_service.update_driver(driver_id, update_data)
        return updated_driver

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


# ORDERS
@driver_router.get(
    "/orders", status_code=status.HTTP_200_OK, dependencies=[Depends(DriverBearer())]
)
def get_available_orders():
    try:
        return order_service.get_available_orders_for_drivers()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}") from e


@driver_router.get(
    "/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(DriverBearer())]
)
def get_order_by_id(order_id: int):
    try:
        order = order_service.get_order_by_id(order_id)
        if order.order_state != OrderState.PREPARED:
            raise HTTPException(
                status_code=400,
                detail=f"This order cannot isn't available, current state : {order.order_state}",
            )

        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}") from e


# DELIVERIES
@driver_router.put(
    "/orders/{order_id}/start",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def start_delivery(order_id: int, driver_id: int = Depends(get_driver_id_from_token)):
    try:
        order = order_service.get_order_by_id(order_id)
        if order.order_state != OrderState.PREPARED:
            raise HTTPException(
                status_code=400,
                detail=f"This order isn't prepared yet, current state : {order.order_state}",
            )
        return driver_service.start_delivery(order_id, driver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting delivery: {e}") from e


@driver_router.get(
    "/orders/{order_id}/path",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def get_path(order_id: int = Depends(get_current_order_id)):
    try:
        order = order_service.get_order_by_id(order_id)
        address = customer_service.get_address_by_customer_id(order.order_customer_id)
        return gm_service.get_path(str(address))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching path: {e}") from e


@driver_router.put(
    "/orders/{order_id}/end",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def end_delivery(
    order_id: int = Depends(get_current_order_id),
    driver_id: int = Depends(get_driver_id_from_token),
):
    try:
        return driver_service.end_delivery(order_id, driver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finishing delivery: {e}") from e
