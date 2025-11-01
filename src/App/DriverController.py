from typing import Annotated

import phonenumbers as pn
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .init_app import customer_service, driver_service, gm_service, jwt_service, order_service
from .JWTBearer import DriverBearer

driver_router = APIRouter(
    prefix="/drivers", tags=["Drivers"], dependencies=[Depends(DriverBearer())]
)


def get_driver_id_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(DriverBearer())],
) -> int:
    token = credentials.credentials
    driver_id = int(jwt_service.validate_user_jwt(token))
    return driver_id


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
    first_name: str = None,
    last_name: str = None,
    phone: str = None,
    driver_id: int = Depends(get_driver_id_from_token),
):
    try:
        update_data = {}
        if first_name:
            update_data["driver_first_name"] = first_name
        if last_name:
            update_data["driver_last_name"] = last_name

        if phone:
            phone_number = pn.parse(phone, "FR")
            if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
                raise ValueError(f"The number {phone} is invalid.")

            driver_phone = "0" + str(phone_number.national_number)
            update_data["driver_phone"] = driver_phone

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
        return order_service.get_paid_orders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}") from e


@driver_router.get(
    "/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(DriverBearer())]
)
def get_order_by_id(order_id: int):
    try:
        order = order_service.get_order_by_id(order_id)
        if not order.order_is_paid or order.order_state != 0:
            raise HTTPException(status_code=400, detail="This order cannot isn't available.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}") from e


# DELIVERIES
@driver_router.put(
    "/orders/{order_id}/accept",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def accept_order(order_id: int, driver_id: int = Depends(get_driver_id_from_token)):
    try:
        order = order_service.get_order_by_id(order_id)
        if not order.order_is_paid:
            raise HTTPException(status_code=400, detail="This order isn't paid.")

        return driver_service.accept_order(order_id, driver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@driver_router.put(
    "/orders/{order_id}/start",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def start_delivery(order_id: int, driver_id: int = Depends(get_driver_id_from_token)):
    try:
        order = order_service.get_order_by_id(order_id)
        if not order.order_is_prepared:
            raise HTTPException(status_code=400, detail="This order isn't prepared yet.")
        return order
        return driver_service.start_delivery(order_id, driver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@driver_router.get(
    "/orders/{order_id}/path",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def get_path(order_id: int):
    order = order_service.get_order_by_id(order_id)
    address = customer_service.get_address_by_customer_id(order.order_customer_id)

    return gm_service.get_path(str(address))


@driver_router.put(
    "/orders/{order_id}/end",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(DriverBearer())],
)
def end_delivery(order_id: int, driver_id: int = Depends(get_driver_id_from_token)):
    try:
        return driver_service.end_delivery(order_id, driver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
