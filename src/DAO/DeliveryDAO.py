from typing import Optional

from src.Model.Delivery import Delivery
from src.Model.order import Order
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class DeliveryDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def get_delivery_by_id(self, order_id: int) -> Optional[Order]:
        raw_order = self.db_connector.sql_query(
            "SELECT * from Order WHERE id=%s", [order_id], "one"
        )
        if raw_order is None:
            return None
        # pyrefly: ignore
        return Order(**raw_order)

    def get_all_order(self) -> Optional[list[Order]]:
        raw_orders = self.db_connector.sql_query("SELECT * from Order", [], "all")
        if raw_orders is None:
            return None
        # pyrefly: ignore
        Orders = [Order(**raw_order) for raw_order in raw_orders]

        return Orders

    def get_all_orders_from_user_id(self, user_id) -> Optional[list[Order]]:
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Order WHERE customer_id=%s", [user_id], "all"
        )
        if raw_orders is None:
            return None
        # pyrefly: ignore
        Orders = [Order(**raw_order) for raw_order in raw_orders]

        return Orders

    def create_delivery(self, order_id, driver_id) -> Delivery:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_created_delivery = self.db_connector.sql_query(
            """
        INSERT INTO Delivery (order_id, driver_id, delivery_state)
        VALUES (%(order_id)s, %(driver_id)s, DEFAULT)
        RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 2},
            "one",
        )
        # pyrefly: ignore

        return Delivery(**raw_created_delivery)

    def update_order(self, order_id, is_paid, is_prepared) -> Order:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_update_order = self.db_connector.sql_query(
            """
        UPDATE Order SET order_is_paid=%(is_paid)s, order_is_prepared=%(is_prepared)s
        WHERE order_id=%(order_id)s RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 1},
            "one",
        )
        # pyrefly: ignore

        return Order(**raw_update_order)

    def delete_order(self, order_id) -> None:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_delete_order = self.db_connector.sql_query(
            """
        DELETE FROM Order WHERE order_id=%s RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 1},
            "one",
        )
        # pyrefly: ignore

        return Order(**raw_delete_order)
