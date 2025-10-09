from fastapi import APIRouter, HTTPException, status

# from src.Model.Item import Item
from src.Service.ItemService import ItemService

item_router = APIRouter(prefix="/items", tags=["Items"])


@item_router.get("/{item_id}", status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: int):
    try:
        # my_movie = movie_service.get_by_id(tmdb_id)
        item = ItemService().get_item_(item_id)
        return item
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Item with id [{}] not found".format(item_id),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception
