from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import Item


class ItemService:
    item_dao: ItemDAO

    def __init__(self, item_dao: ItemDAO):
        self.item_dao = item_dao

    def get_item(self, item_id: int) -> Item | None:
        print(f"[ItemService] Getting item with ID: {item_id}")
        item = self.item_dao.get_item_by_id(item_id)
        print(f"[ItemService] DAO returned: {item}")
        return item

    def get_all_item(self) -> list[Item] | None:
        print("[ItemService] Getting all items")
        items = self.item_dao.get_all_item()
        print(f"[ItemService] DAO returned: {items}")
        return items

    def create_item(
        self, id: int, name: str, price: int, type: str, description: str, stock: int
    ) -> None:
        print(
            f"[ItemService] Creating item: item_name={name}, item_price={price},\n"
            f"  item_type={type}, item_description={description}, item_stock={stock}"
        )

        new_item = Item(
            item_id=id,
            item_name=name,
            item_price=price,
            item_type=type,
            item_description=description,
            item_stock=stock,
        )

        print(f"[ItemService] New Item object created: {new_item}")

        created_item = self.item_dao.create_item(
            item_id=id,
            item_name=name,
            item_price=price,
            item_type=type,
            item_description=description,
            item_stock=stock,
        )
        print(f"[ItemService] DAO returned after creation: {created_item}")
        return created_item

    def update_item(self, id: int, update) -> None:
        update_message_parts = []
        for field, value in update.items():
            update_message_parts.append(f"{field}={value}")

        print(f"[ItemService] Updating item: {', '.join(update_message_parts)}")

        updated_item = self.item_dao.update_item(item_id=id, update=update)
        print(f"[ItemService] DAO returned after creation: {updated_item}")
        return updated_item

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
        print(f"[ItemService] Adding item ID {item_id} (x{quantity}) to order {order.id_order}")
        item = self.item_dao.get_item_by_id(item_id)
        # Check if Item exist
        if item is None:
            raise ValueError(f"[ItemService] Item with ID {item_id} not found.")

        # Check the Stock
        if item.stock < quantity:
            raise ValueError(
                f"[ItemService] Not enough stock for '{item.name}' (available: {item.stock})."
            )

        order.items.append(item)
        print(f"[ItemService] Item '{item.name}' added to order {order.id_order}.")
        # Update Stocks
        item.stock -= quantity
        print(f"[ItemService] Updated stock for '{item.name}': {item.stock}")

        self.item_dao.update_item(item)  # A changer quand on aura écrit la méthode
        print(f"[ItemService] Item '{item.name}' persisted after stock update.")

    def delete_item(self, item_id: int) -> None:
        """
        Deletes an item from the database by its ID.

        Parameters
        ----------
        item_id : int
            The ID of the item to delete.
        """
        print(f"[ItemService] Deleting item with ID: {item_id}")

        item = self.item_dao.get_item_by_id(item_id)
        if item is None:
            raise ValueError(f"[ItemService] Cannot delete: item with ID {item_id} not found.")

        self.item_dao.delete_item_by_id(item_id)
        print(f"[ItemService] Item with ID {item_id} has been deleted.")
