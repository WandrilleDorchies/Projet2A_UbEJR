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
