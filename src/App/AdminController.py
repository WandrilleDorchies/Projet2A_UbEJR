from datetime import datetime
from typing import Annotated, Dict

import phonenumbers as pn
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .init_app import (
    bundle_service,
    customer_service,
    driver_service,
    item_service,
    jwt_service,
    menu_service,
    order_service,
)
from .JWTBearer import AdminBearer

admin_router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(AdminBearer())])


def get_admin_id_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(AdminBearer())],
) -> int:
    token = credentials.credentials
    customer_id = int(jwt_service.validate_user_jwt(token))
    return customer_id


# MENU
@admin_router.get(
    "/orderables", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_orderables():
    try:
        return menu_service.get_all_orderables(in_menu=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e


@admin_router.put(
    "/orderables/{orderable_id}/add",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def add_orderable_to_menu(orderable_id: int):
    try:
        menu_service.add_orderable_to_menu(orderable_id)
        return f"The item with Orderable ID {orderable_id} has been added to the menu."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e


@admin_router.put(
    "/orderables/{orderable_id}/remove",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def remove_orderable_from_menu(orderable_id: int):
    try:
        menu_service.remove_orderable_from_menu(orderable_id)
        return f"The item with Orderable ID {orderable_id} has been removed from the menu."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e


# ITEMS
@admin_router.get(
    "/items/{item_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_item_by_id(item_id: int):
    try:
        item = item_service.get_item_by_id(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id [{item_id}] not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.post(
    "/items", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminBearer())]
)
def create_item(
    item_name: str,
    item_price: float,
    item_type: str,
    item_description: str,
    item_stock: int,
):
    try:
        item = item_service.create_item(
            item_name, item_price, item_type, item_description, item_stock
        )
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.put(
    "/items/{item_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def update_item(
    item_id: int,
    item_name: str = None,
    item_price: float = None,
    item_type: str = None,
    item_description: str = None,
    item_stock: int = None,
):
    try:
        update = {}
        update = {
            key: value
            for key, value in [
                ("item_name", item_name),
                ("item_price", item_price),
                ("item_type", item_type),
                ("item_description", item_description),
                ("item_stock", item_stock),
            ]
            if value is not None
        }

        updated_item = item_service.update_item(item_id, update)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.post(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminBearer())],
)
def delete_item(item_id: int):
    try:
        item_service.delete_item(item_id)
        return
    except Exception as e:
        if "foreign key constraint" in str(e):
            raise HTTPException(
                status_code=403, detail=f"Forbidden - cannot delete item in bundles: {e}"
            ) from e
        else:
            raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


# BUNDLES
@admin_router.get(
    "/bundles/{bundle_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_bundle_by_id(bundle_id: int):
    try:
        bundle = bundle_service.get_bundle_by_id(bundle_id)
        if bundle is None:
            raise HTTPException(status_code=404, detail=f"Bundle with id [{bundle_id}] not found")
        return bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.post(
    "/bundles", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminBearer())]
)
def create_bundle(
    bundle_name: str,
    bundle_reduction: int,
    bundle_description: str,
    bundle_availability_start_date: str,
    bundle_availability_end_date: str,
    bundle_items: Dict,
):
    try:
        Items = {}
        for item_id, nb in bundle_items.items():
            item = item_service.get_item_by_id(int(item_id))
            if not item:
                raise ValueError(f"Item with id {item_id} not found")
            Items[item] = nb

        bundle = bundle_service.create_bundle(
            bundle_name,
            bundle_reduction,
            bundle_description,
            datetime.strptime(bundle_availability_start_date, "%d/%m/%Y"),
            datetime.strptime(bundle_availability_end_date, "%d/%m/%Y"),
            Items,
        )
        return bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.put(
    "/bundles/{bundle_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def update_bundle(
    bundle_id: int,
    bundle_name: str = None,
    bundle_reduction: int = None,
    bundle_description: str = None,
    bundle_availability_start_date: datetime = None,
    bundle_availability_end_date: datetime = None,
    bundle_items: Dict[int, int] = None,
):
    try:
        update = {}
        update = {
            key: value
            for key, value in [
                ("bundle_name", bundle_name),
                ("bundle_reduction", bundle_reduction),
                ("bundle_description", bundle_description),
                (
                    "bundle_availability_start_date",
                    datetime.strptime(bundle_availability_start_date, "%d/%m/%Y"),
                ),
                (
                    "bundle_availability_end_date",
                    datetime.strptime(bundle_availability_end_date, "%d/%m/%Y"),
                ),
            ]
            if value is not None
        }
        if bundle_items:
            Items = {}
            for item_id, nb in bundle_items.items():
                item = item_service.get_item_by_id(int(item_id))
                if not item:
                    raise ValueError(f"Item with id {item_id} not found")
                Items[item] = nb
            update["bundle_items"] = Items

        updated_bundle = bundle_service.update_bundle(bundle_id, update)
        return updated_bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.post(
    "/bundles/{bundle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminBearer())],
)
def delete_bundle(bundle_id: int):
    try:
        bundle_service.delete_bundle(bundle_id)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


# CUSTOMERS
@admin_router.get(
    "/customers", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_customers():
    try:
        return customer_service.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.get(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def get_customer_by_id(customer_id: int):
    try:
        return customer_service.get_customer_by_id(customer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.delete(
    "/customers/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminBearer())],
)
def delete_customer(customer_id: int):
    try:
        return customer_service.delete_customer(customer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.put(
    "/customer", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def update_profile(
    customer_id: int,
    first_name: str = None,
    last_name: str = None,
    mail: str = None,
    phone: str = None,
):
    try:
        customer_service.get_customer_by_id(customer_id)
        update_data = {}
        if first_name:
            update_data["customer_first_name"] = first_name
        if last_name:
            update_data["customer_last_name"] = last_name
        if mail:
            update_data["customer_mail"] = mail

        if phone:
            phone_number = pn.parse(phone, "FR")
            if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
                raise ValueError(f"The number {phone} is invalid.")

            customer_phone = "0" + str(phone_number.national_number)
            update_data["customer_phone"] = customer_phone

        updated_customer = customer_service.update_customer(customer_id, update_data)
        return updated_customer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


# DRIVERS
@admin_router.post(
    "/drivers", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminBearer())]
)
def create_driver(
    first_name: str, last_name: str, phone: str, password: str, confirm_password: str
):
    try:
        if confirm_password != password:
            raise HTTPException(status_code=400, detail="The two password don't match.")
        return driver_service.create_driver(first_name, last_name, phone, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e


@admin_router.get("/drivers", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())])
def get_all_drivers():
    try:
        return driver_service.get_all_drivers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.get(
    "/drivers/{driver_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def get_driver_by_id(driver_id: int):
    try:
        return driver_service.get_driver_by_id(driver_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.delete(
    "/drivers/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminBearer())],
)
def delete_driver(driver_id: int):
    try:
        return driver_service.delete_driver(driver_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_router.put(
    "/drivers/{customer_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AdminBearer())],
)
def update_driver(
    driver_id: int,
    first_name: str = None,
    last_name: str = None,
    phone: str = None,
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
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


# ORDERS
@admin_router.get("/orders", status_code=status.HTTP_200_OK)
def get_all_orders():
    try:
        return order_service.get_all_order()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}") from e


@admin_router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order(order_id: int):
    try:
        return order_service.get_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@admin_router.put("/orders/{order_id}/prepared", status_code=status.HTTP_200_OK)
def mark_order_as_prepared(order_id: int):
    try:
        update_data = {"order_is_prepared": True}
        updated_order = order_service.update_order(order_id, update_data)
        return updated_order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# OVERVIEW
@admin_router.get(
    "/overview", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_overview():
    try:
        customers = customer_service.get_all_customers()
        drivers = driver_service.get_all_drivers()
        orders = order_service.get_all_orders()
        orders_prepared = order_service.get_all_orders_prepared()
        current_orders = order_service.get_current_orders()
        benef = [order.price for order in order_service.get_past_orders()]
        items = menu_service.get_all_orderables(in_menu=True)

        return {
            "total_customers": len(customers) if customers else 0,
            "total_drivers": len(drivers) if drivers else 0,
            "total_orders": len(orders) if orders else 0,
            "total_orders_prepared": len(orders_prepared) if orders_prepared else 0,
            "total_current_orders": len(current_orders) if current_orders else 0,
            "total_orderables_in_menu": len(items) if items else 0,
            "benefice": f"{sum(benef)} €",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching datas: {e}") from e
