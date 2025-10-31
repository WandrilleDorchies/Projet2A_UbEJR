from datetime import datetime
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .init_app import (
    bundle_service,
    # customer_service,
    # driver_service,
    # order_service,
    item_service,
    jwt_service,
    menu_service,
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
        return menu_service.get_all_orderable(in_menu=False)

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e


# ITEMS
@admin_router.get(
    "items/{item_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
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
