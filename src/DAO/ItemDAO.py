from typing import Optional

from src.Model.Item import Item
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class ItemDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    # CREATE
    def create_item(self, item_name, item_price, item_type, item_description, item_stock) -> Item:
        raw_created_item = self.db_connector.sql_query(
            """
        INSERT INTO Items (id_item, name, price, item_type, description, stock)
        VALUES (DEFAULT, %(item_name)s, %(item_price)s, %(item_type)s, %(item_description)s, %(item_stock)s)
        RETURNING *;
        """,
            {
                "item_name": item_name,
                "item_price": item_price,
                "item_type": item_type,
                "item_description": item_description,
                "item_stock": item_stock,
            },
            "one",
        )
        # pyrefly: ignore

        return Item(**raw_created_item)

    # READ
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * from Items WHERE item_id=%s", [item_id], "one"
        )
        if raw_item is None:
            return None
        # pyrefly: ignore
        return Item(**raw_item)

    def get_all_items(self) -> Optional[list[Item]]:
        raw_items = self.db_connector.sql_query("SELECT * from Item", [], "all")
        if raw_items is None:
            return None
        # pyrefly: ignore
        Items = [Item(**raw_item) for raw_item in raw_items]
        return Items

    # UPDATE

    # DELETE

    def delete_item_by_id(self, item_id) -> None:
        # TODO: prevent deleting items present in Bundle_Items
        self.db_connector.sql_query(
            "DELETE * FROM Item WHERE item_id = %(item_id)s", {"item_id": item_id}, None
        )
