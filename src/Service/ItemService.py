from typing import List, Optional

from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Item import Item
from src.utils.log_decorator import log


class ItemService:
    item_dao: ItemDAO
    order_dao: OrderDAO

    def __init__(self, item_dao: ItemDAO, order_dao: OrderDAO):
        self.item_dao = item_dao
        self.order_dao = order_dao

    @log
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        item = self.item_dao.get_item_by_id(item_id)
        if item is None:
            raise ValueError(f"[ItemService] Cannot get: item with ID {item_id} not found.")
        return item

    @log
    def get_all_items(self) -> Optional[List[Item]]:
        items = self.item_dao.get_all_items()
        return items

    @log
    def create_item(
        self,
        item_name: str,
        item_price: int,
        item_type: str,
        item_description: str,
        item_stock: int,
        item_image: bytes,
        is_in_menu: bool = False,
    ) -> Optional[Item]:
        created_item = self.item_dao.create_item(
            item_name=item_name,
            item_price=item_price,
            item_type=item_type,
            item_description=item_description,
            item_stock=item_stock,
            item_image=item_image,
            is_in_menu=is_in_menu,
        )
        return created_item

    @log
    def update_item(self, item_id: int, update: dict) -> Optional[Item]:
        item = self.item_dao.update_item(item_id, update=update)
        if item is None:
            raise ValueError(f"[ItemService] Cannot update: item with ID {item_id} not found.")
        return item

    @log
    def delete_item(self, item_id: int) -> None:
        """
        Deletes an item from the database by its ID.

        Parameters
        ----------
        item_id : int
            The ID of the item to delete.
        """
        item = self.item_dao.get_item_by_id(item_id)
        if item is None:
            raise ValueError(f"[ItemService] Cannot delete: item with ID {item_id} not found.")

        self.item_dao.delete_item_by_id(item_id)
