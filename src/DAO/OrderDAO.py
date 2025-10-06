from typing import Optional

from src.Model.Order import Order
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class OrderDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
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

    def create_order(self, customer_id, order_state, order_date, order_time) -> Order:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_created_order = self.db_connector.sql_query(
            """
        INSERT INTO Order (order_id, customer_id, order_state, order_date, order_time, order_is_paid, order_is_prepared)
        VALUES (DEFAULT, %(customer_id)s, %(state)s, %(order_date)s, %(order_time)s, DEFAULT, DEFAULT)
        RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 2},
            "one",
        )
        # pyrefly: ignore

        return Order(**raw_created_order)

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
