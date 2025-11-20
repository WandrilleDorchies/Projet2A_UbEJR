from fastapi import APIRouter, Depends, HTTPException, status

from src.App.init_app import (
    customer_service,
    driver_service,
)
from src.App.JWTBearer import AdminBearer

admin_users_router = APIRouter(prefix="", tags=["Users"], dependencies=[Depends(AdminBearer())])


# CUSTOMERS
@admin_users_router.get(
    "/customers", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_customers():
    try:
        return customer_service.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_users_router.get(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def get_customer_by_id(customer_id: int):
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        if customer is None:
            raise HTTPException(
                status_code=404, detail=f"Customer with id [{customer_id}] not found"
            )
        return customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_users_router.delete(
    "/customers/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminBearer())],
)
def delete_customer(customer_id: int):
    try:
        return customer_service.delete_customer(customer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_users_router.put(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def update_profile(
    customer_id: int,
    customer_first_name: str = None,
    customer_last_name: str = None,
    customer_mail: str = None,
    customer_phone: str = None,
):
    try:
        update_data = locals()
        update_data.pop("customer_id")
        updated_customer = customer_service.update_customer(customer_id, update_data)
        return updated_customer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


# DRIVERS
@admin_users_router.post(
    "/drivers", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminBearer())]
)
def create_driver(
    first_name: str, last_name: str, phone: str, password: str, confirm_password: str
):
    try:
        if confirm_password != password:
            raise HTTPException(status_code=400, detail="The two password don't match.")
        if customer_service.get_customer_by_phone(phone):
            raise HTTPException(
                status_code=403,
                detail="[AdminController] Cannot update driver: "
                "A customer already have this phone number.",
            )
        return driver_service.create_driver(first_name, last_name, phone, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e


@admin_users_router.get(
    "/drivers", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_drivers():
    try:
        return driver_service.get_all_drivers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_users_router.get(
    "/drivers/{driver_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def get_driver_by_id(driver_id: int):
    try:
        driver = driver_service.get_driver_by_id(driver_id)
        if driver is None:
            raise HTTPException(status_code=404, detail=f"Driver with id [{driver_id}] not found")
        return driver
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_users_router.delete(
    "/drivers/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminBearer())],
)
def delete_driver(driver_id: int):
    try:
        return driver_service.delete_driver(driver_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_users_router.put(
    "/drivers/{driver_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AdminBearer())],
)
def update_driver(
    driver_id: int,
    driver_first_name: str = None,
    driver_last_name: str = None,
    driver_phone: str = None,
):
    try:
        update_data = locals()
        update_data.pop("driver_id")
        if update_data.get("driver_phone") and customer_service.get_customer_by_phone(driver_phone):
            raise HTTPException(
                status_code=403,
                detail="[AdminController] Cannot update driver: "
                "A customer already have this phone number.",
            )
        updated_driver = driver_service.update_driver(driver_id, update_data)
        return updated_driver

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e
