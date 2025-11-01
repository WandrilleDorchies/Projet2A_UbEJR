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
        item_image: bytes,
        is_in_menu: bool = False,
    ) -> Item:
        orderable_id = self.orderable_dao.create_orderable(
            "item", item_image, item_name, is_in_menu
        )
        raw_item = self.db_connector.sql_query(
            """
            INSERT INTO Items (orderable_id, item_name, item_price, item_type,
            item_description, item_stock)
            VALUES (%(orderable_id)s, %(item_name)s, %(item_price)s, %(item_type)s,
            %(item_description)s, %(item_stock)s)
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
        raw_item["is_in_menu"] = is_in_menu
        return Item(**raw_item)

    # READ
    @log
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * from Items WHERE item_id=%s", [item_id], "one"
        )
        if raw_item is None:
            return None

        raw_item["is_in_menu"] = self.orderable_dao._is_in_menu(raw_item["orderable_id"])
        raw_item["orderable_image"] = self.orderable_dao.get_image_from_orderable(
            raw_item["orderable_id"]
        )

        return Item(**raw_item)

    @log
    def get_item_by_orderable_id(self, orderable_id: int) -> Optional[Item]:
        raw_item = self.db_connector.sql_query(
            "SELECT * FROM Items WHERE orderable_id=%s", [orderable_id], "one"
        )
        if raw_item is None:
            return None

        raw_item["is_in_menu"] = self.orderable_dao._is_in_menu(raw_item["orderable_id"])
        raw_item["orderable_image"] = self.orderable_dao.get_image_from_orderable(
            raw_item["orderable_id"]
        )
        return Item(**raw_item)

    @log
    def get_all_items(self) -> List[Item]:
        raw_items = self.db_connector.sql_query("SELECT * from Items", return_type="all")

        if not raw_items:
            return []

        Items = []
        for raw_item in raw_items:
            raw_item["is_in_menu"] = self.orderable_dao._is_in_menu(raw_item["orderable_id"])
            raw_item["orderable_image"] = self.orderable_dao.get_image_from_orderable(
                raw_item["orderable_id"]
            )
            Items.append(Item(**raw_item))

        return Items

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
            "item_image",
        ]
        for key in update.keys():
            if key not in parameters_update:
                raise ValueError(f"{key} is not a parameter of Item.")

        if update.get("item_image"):
            item = self.get_item_by_id(item_id)
            orderable_id = item.orderable_id
            item_name = update.get("item_name") if update.get("item_name") else item.item_name
            self.orderable_dao.update_image(orderable_id, "item", item_name, update["item_image"])
            update.pop("item_image")

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
        item = self.get_item_by_id(item_id)
        self.orderable_dao.delete_orderable(item.orderable_id)
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
