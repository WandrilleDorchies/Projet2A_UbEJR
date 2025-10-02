from typing import Optional

from src.Model.item import Item

from .DBConnector import DBConnector


class ItemDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query("SELECT * from Items WHERE id=%s", [item_id], "one")
        if raw_item is None:
            return None
        # pyrefly: ignore
        return Item(**raw_item)

    def create_item(self, name, price, type_item, description, stock) -> Item:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_created_item = self.db_connector.sql_query(
            """
        INSERT INTO Items (id_item, name, price, type, description, stock)
        VALUES (DEFAULT, %(name)s, %(price)s,%(type_item)s, %(description)s, %(stock)s)
        RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 1},
            "one",
        )
        # pyrefly: ignore

        return Item(**raw_created_item)
