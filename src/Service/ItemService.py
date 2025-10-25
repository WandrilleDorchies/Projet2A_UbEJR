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
    def get_item(self, item_id: int) -> Optional[Item]:
        item = self.item_dao.get_item_by_id(item_id)
        return item

    @log
    def get_all_item(self) -> Optional[List[Item]]:
        items = self.item_dao.get_all_item()
        return items

    @log
    def create_item(
        self,
        item_name: str,
        item_price: int,
        item_type: str,
        item_description: str,
        item_stock: int,
    ) -> Optional[Item]:

        created_item = self.item_dao.create_item(
            item_name=item_name,
            item_price=item_price,
            item_type=item_type,
            item_description=item_description,
            item_stock=item_stock,
        )
        return created_item

    @log
    def update_item(self, item_id: int, update) -> Optional[Item]:
        update_message_parts = []
        for field, value in update.items():
            update_message_parts.append(f"{field}={value}")

        updated_item = self.item_dao.update_item(item_id=item_id, update=update)
        return updated_item

    @log
    def add_to_order(self, item_id: int, order, quantity: int = 1) -> None:
        """
        Adds an item to a given order if enough stock is available.

        Parameters
        ----------
        item_id : int
            ID of the item to add.
        order : Order
            The order to which the item will be added.
        quantity : int, optional
            Number of units to add (default is 1).
        """
        item = self.item_dao.get_item_by_id(item_id)
        if item is None:
            raise ValueError(f"[ItemService] Item with ID {item_id} not found.")

        if item.item_stock < quantity:
            raise ValueError(
                f"[ItemService] Not enough stock for '{item.name}' (available: {item.stock})."
            )

        update_data = {"item_stock": item.item_stock - quantity}
        self.item_dao.update_item(item.item_id, update_data)

        self.order_dao.add_orderable_to_order(item.orderable_id, quantity)

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
