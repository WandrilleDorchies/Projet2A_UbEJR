from typing import List, Optional

from src.Model.Item import Item
from src.utils.log_decorator import log
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
    @log
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
    @log
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * from Items WHERE item_id=%s", [item_id], "one"
        )
        return Item(**raw_item) if raw_item else None

    @log
    def get_item_by_orderable_id(self, orderable_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * FROM Items WHERE orderable_id=%s", [orderable_id], "one"
        )
        return Item(**raw_item) if raw_item else None

    @log
    def get_all_items(self) -> Optional[List[Item]]:
        raw_items = self.db_connector.sql_query("SELECT * from Items", return_type="all")
        return [Item(**raw_item) for raw_item in raw_items] if raw_items else None

    # UPDATE
    @log
    def update_item(self, item_id: int, update: dict) -> Item:
        if not update:
            raise ValueError("At least one value should be updated")

        parameters_update = [
            "item_name",
            "item_price",
            "item_type",
            "item_description",
            "item_stock",
            "item_in_menu",
        ]
        for key in update.keys():
            if key not in parameters_update:
                raise ValueError(f"{key} is not a parameter of Item.")

        updated_fields = [f"{field} = %({field})s" for field in update.keys()]
        set_field = ", ".join(updated_fields)
        params = {**update, "item_id": item_id}

        self.db_connector.sql_query(
            f"""
            UPDATE Items
            SET {set_field}
            WHERE item_id = %(item_id)s;
            """,
            params,
            "none",
        )

        return self.get_item_by_id(item_id)

    # DELETE
    @log
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
