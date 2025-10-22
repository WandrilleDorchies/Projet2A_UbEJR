from typing import Dict, List, Optional

from src.Model.Item import Item
from src.utils.singleton import Singleton

from .DBConnector import DBConnector
from .OrderableDAO import OrderableDAO


class ItemDAO(metaclass=Singleton):
    db_connector: DBConnector
    orderable_dao: OrderableDAO

    def __init__(self, db_connector: DBConnector, orderable_dao: OrderableDAO):
        self.db_connector = db_connector
        self.orderable_dao = orderable_dao

    # CREATE
    def create_item(
        self,
        item_name: str,
        item_price: float,
        item_type: str,
        item_description: str,
        item_stock: int,
    ) -> Item:
        orderable_id = self.orderable_dao.create_orderable("item")
        raw_item = self.db_connector.sql_query(
            """
            INSERT INTO Items (orderable_id, item_name, item_price, item_type,
            item_description, item_stock, item_in_menu)
            VALUES (%(orderable_id)s, %(item_name)s, %(item_price)s, %(item_type)s,
            %(item_description)s, %(item_stock)s, DEFAULT)
            RETURNING *;
            """,
            {
                "orderable_id": orderable_id,
                "item_name": item_name,
                "item_price": item_price,
                "item_type": item_type,
                "item_description": item_description,
                "item_stock": item_stock,
            },
            "one",
        )
        return Item(**raw_item)

    # READ
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * from Items WHERE item_id=%s", [item_id], "one"
        )
        return Item(**raw_item) if raw_item else None

    def get_item_by_orderable_id(self, orderable_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * FROM Items WHERE orderable_id=%s", [orderable_id], "one"
        )
        return Item(**raw_item) if raw_item else None

    def get_all_items(self) -> Optional[List[Item]]:
        raw_items = self.db_connector.sql_query("SELECT * from Items", "all")
        return [Item(**raw_item) for raw_item in raw_items] if raw_items else None

    # UPDATE
    def update_item(
        self,
        item_id: int,
        item_name: str,
        item_price: float,
        item_type: str,
        item_description: str,
        item_stock: int,
        item_in_menu: bool,
    ) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            """
            UPDATE Items
            SET item_name = %(item_name)s,
                item_price = %(item_price)s,
                item_type = %(item_type)s,
                item_description = %(item_description)s,
                item_stock = %(item_stock)s,
                item_in_menu = %(item_in_menu)s
            WHERE item_id=%s
            RETURNING *;
            """,
            {
                "item_name": item_name,
                "item_price": item_price,
                "item_type": item_type,
                "item_description": item_description,
                "item_stock": item_stock,
                "item_in_menu": item_in_menu,
            },
            "one",
        )
        return Item(**raw_item)

    # DELETE
    def delete_item_by_id(self, item_id: int) -> None:
        if self._item_is_in_bundle(item_id):
            raise ValueError("The item is in a bundle and cannot be deleted.")

        self.db_connector.sql_query(
            "DELETE FROM Items WHERE item_id = %(item_id)s", {"item_id": item_id}, None
        )

    def _item_is_in_bundle(self, item_id: int) -> bool:
        result = self.db_connector.sql_query(
            """SELECT COUNT(*)
               FROM Bundle_Items WHERE item_id = %(item_id)s;
             """,
            {"item_id": item_id},
            "one",
        )
        return result["count"] > 0

    def _get_items_in_order(self, order_id: int) -> Optional[Dict[Item, int]]:
        raw_items = self.db_connector.sql_query(
            """
            SELECT i.*, oi.item_quantity
            FROM Items as i
            INNER JOIN Order_Items AS oi ON i.item_id=oi.item_id
            WHERE oi.order_id=%s;
            """,
            [order_id],
            "all",
        )
        if not raw_items:
            return None

        item_attributes = [dict(list(raw_item.items())[:-1]) for raw_item in raw_items]
        quantities = [raw_item["item_quantity"] for raw_item in raw_items]
        items = [Item(**item_attribute) for item_attribute in item_attributes]

        items_in_order = {item: quantity for item, quantity in zip(items, quantities, strict=False)}
        return items_in_order
