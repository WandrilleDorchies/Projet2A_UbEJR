import traceback

from fastapi import APIRouter, HTTPException, status

from src.App.init_app import item_service

# from src.Model.Item import Item
# from src.Service.ItemService import ItemService

item_router = APIRouter(prefix="/items", tags=["Items"])


@item_router.get("/{item_id}", status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: int):
    try:
        print(f"DEBUG: Calling item_service.get_item({item_id})")
        item = item_service.get_item(item_id)
        print(f"DEBUG: item_service returned: {item}")
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id [{item_id}] not found")
        return item
    except Exception as e:
        print("ERROR: Exception caught in controller")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@item_router.get("/", status_code=status.HTTP_200_OK)
def get_all_item():
    try:
        print("DEBUG: Calling item_service.get_all_item()")
        items = item_service.get_all_item()
        print(f"DEBUG: item_service returned: {items}")
        if items is None:
            raise HTTPException(status_code=404, detail="Nothing found")
        return items
    except Exception as e:
        print("ERROR: Exception caught in controller")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@item_router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(
    item_id: int,
    item_name: str,
    item_price: float,
    item_type: str,
    item_description: str,
    item_stock: int,
):
    try:
        print(
            f"DEBUG: Calling item_service.create_item({
                item_id, item_name, item_price, item_type, item_description, item_stock
            })"
        )
        item = item_service.create_item(
            item_id, item_name, item_price, item_type, item_description, item_stock
        )
        print(f"DEBUG: item_service returned: {item}")
        return item
    except Exception as e:
        print("ERROR: Exception caught in controller")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e


@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    try:
        print(f"DEBUG: Calling item_service.delete_item({item_id})")
        item_service.delete_item(item_id)
        print(f"DEBUG: item_service deleted item {item_id}")
        return
    except Exception as e:
        print("ERROR: Exception caught in controller")
        traceback.print_exc()
        if "foreign key constraint" in str(e):
            raise HTTPException(
                status_code=403, detail=f"Forbidden - cannot delete item in bundles: {e}"
            ) from e
        else:
            raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e
