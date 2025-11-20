from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from src.App.init_app import (
    bundle_service,
    item_service,
    menu_service,
)
from src.App.JWTBearer import AdminBearer
from src.Model.Item import ITEM_TYPE

admin_orderables_router = APIRouter(
    prefix="", tags=["Menu / Orderables"], dependencies=[Depends(AdminBearer())]
)


# MENU
@admin_orderables_router.get(
    "/orderables", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_orderables(in_menu: bool = False):
    try:
        return menu_service.get_all_orderables(in_menu=in_menu)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e


@admin_orderables_router.post(
    "/orderables/{orderable_id}/add",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def add_orderable_to_menu(orderable_id: int):
    try:
        menu_service.add_orderable_to_menu(orderable_id)
        return f"The item with Orderable ID {orderable_id} has been added to the menu."
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"[AdminController] Cannot add orderable to menu : {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {str(e)}") from e


@admin_orderables_router.delete(
    "/orderables/{orderable_id}/remove",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AdminBearer())],
)
def remove_orderable_from_menu(orderable_id: int):
    try:
        menu_service.remove_orderable_from_menu(orderable_id)
        return f"The item with Orderable ID {orderable_id} has been removed from the menu."
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"[AdminController] Cannot remove orderable from menu : {str(e)}",
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e


# ITEMS
@admin_orderables_router.get(
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


@admin_orderables_router.post(
    "/items", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminBearer())]
)
async def create_item(
    item_name: str,
    item_price: float,
    item_type: ITEM_TYPE,
    item_description: str,
    item_stock: int,
    item_image: Optional[str] = None,
):
    try:
        item = item_service.create_item(
            item_name, item_price, item_type, item_description, item_stock, item_image
        )
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_orderables_router.put(
    "/items/{item_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
async def update_item(
    item_id: int,
    item_name: str = None,
    item_price: float = None,
    item_type: ITEM_TYPE = None,
    item_description: str = None,
    item_stock: int = None,
    item_image: Optional[str] = None,
):
    try:
        update = locals()
        update.pop("item_id")
        updated_item = item_service.update_item(item_id, update)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_orderables_router.delete(
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
@admin_orderables_router.get(
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


query_item_id = Query(None, description="IDs des items à ajouter")
query_item_quantities = Query(None, description="Quantités correspondantes")


@admin_orderables_router.post(
    "/bundles", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminBearer())]
)
async def create_bundle(
    bundle_name: str,
    bundle_reduction: int,
    bundle_description: str,
    bundle_availability_start_date: str,
    bundle_availability_end_date: str,
    item_ids: list[int] = query_item_id,
    item_quantities: list[int] = query_item_quantities,
    bundle_image: Optional[str] = None,
):
    try:
        if len(item_ids) != len(item_quantities):
            raise ValueError("The number of item and quantities does not match.")

        if any([item_quantity <= 0 for item_quantity in item_quantities]):
            raise ValueError("All items in the bundle must be in positive quantity.")
        Items = {}
        for item_id, nb in zip(item_ids, item_quantities, strict=False):
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
            bundle_image,
        )
        return bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_orderables_router.put(
    "/bundles/{bundle_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
async def update_bundle(
    bundle_id: int,
    bundle_name: str = None,
    bundle_reduction: int = None,
    bundle_description: str = None,
    bundle_availability_start_date: datetime = None,
    bundle_availability_end_date: datetime = None,
    item_ids: Optional[list[int]] = query_item_id,
    item_quantities: Optional[list[int]] = query_item_quantities,
    bundle_image: Optional[str] = None,
):
    try:
        update = locals()
        update.pop("item_ids")
        update.pop("item_quantities")
        update.pop("bundle_id")

        if item_ids and item_quantities:
            if len(item_ids) != len(item_quantities):
                raise ValueError("The number of item and quantities does not match.")
            Items = {}
            for item_id, nb in zip(item_ids, item_quantities, strict=False):
                item = item_service.get_item_by_id(int(item_id))
                if not item:
                    raise ValueError(f"Item with id {item_id} not found")
                Items[item] = nb
            update["bundle_items"] = Items

        updated_bundle = bundle_service.update_bundle(bundle_id, update)
        return updated_bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@admin_orderables_router.delete(
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


@admin_orderables_router.get(
    "/orderables/{orderable_id}/image", status_code=status.HTTP_200_OK, response_class=Response
)
def get_orderable_image(orderable_id: int):
    try:
        image_data = menu_service.get_orderable_image(orderable_id)
        if image_data is None:
            raise HTTPException(status_code=404, detail="Image not found")

        return Response(content=image_data, media_type="image/jpg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image: {e}") from e
