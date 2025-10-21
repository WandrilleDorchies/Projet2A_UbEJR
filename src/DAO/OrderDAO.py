from datetime import datetime
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
            """SELECT o.*, oi.
               FROM Orders as o
               INNER JOIN Orders_Items as oi
               ON o.order_id=oi.order_id WHERE order_id='%s'""",
            [order_id],
            "one",
        )

        if raw_order is None:
            return None
        return Order(**raw_order)

    def get_all_order(self) -> Optional[list[Order]]:
        raw_orders = self.db_connector.sql_query("SELECT * from Orders", [], "all")
        if raw_orders is None:
            return None
        Orders = [Order(**raw_order) for raw_order in raw_orders]

        return Orders

    def get_all_orders_from_user_id(self, user_id: int) -> Optional[list[Order]]:
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Orders WHERE order_customer_id=%s", [user_id], "all"
        )
        if raw_orders is None:
            return None
        Orders = [Order(**raw_order) for raw_order in raw_orders]

        return Orders

    def create_order(self, customer_id: int, order_state: str, order_date: datetime) -> Order:
        raw_created_order = self.db_connector.sql_query(
            """
        INSERT INTO Order (order_id,
                           order_customer_id,
                           order_state,
                           order_date,
                           order_time,
                           order_is_paid,
                           order_is_prepared)
        VALUES (DEFAULT,
                %(customer_id)s,
                '%(order_state)s',
                %(order_date)s
                %(order_time)s
                FALSE,
                FALSE)
        RETURNING *;
        """,
            {
                "customer_id": customer_id,
                "order_state": order_state,
                "order_date": order_date,
                "order_time": datetime.now(),
            },
            "one",
        )
        return Order(**raw_created_order)

    def update_order(self, order_id, is_paid, is_prepared) -> Order:
        raw_update_order = self.db_connector.sql_query(
            """
            UPDATE Order SET order_is_paid=%(is_paid)s, order_is_prepared=%(is_prepared)s
            WHERE order_id=%(order_id)s RETURNING *;
            """,
            {"is_paid": is_paid, "is_prepared": is_prepared, "order_id": order_id},
            "none",
        )
        return Order(**raw_update_order)

    def delete_order(self, order_id) -> None:
        raw_delete_order = self.db_connector.sql_query(
            """
        DELETE FROM Order WHERE order_id=%s RETURNING *;
        """,
            {"key": 1},
            "one",
        )

        return Order(**raw_delete_order)

    def add_item_to_order(self, item_id: int, order_id: int, item_price: float) -> Order:
        if self._get_quantity_of_item(item_id, order_id) >= 1:
            self.db_connector.sql_query(
                """UPDATE Order_Items
                   SET item_quantity=item_quantity+1
                   WHERE order_id=%(order_id)s AND item_id=%(item_id)s;
                """,
                {"order_id": order_id, "item_id": item_id},
                "one",
            )

        else:
            self.db_connector.sql_query(
                """INSERT INTO Order_Items
                   VALUES (%(order_id)s, %(item_id)s, 1, %(item_price)s);
                """,
                {"order_id": order_id, "item_id": item_id, "item_price": item_price},
                "one",
            )

    def remove_item_from_order(self, order_id: int, item_id: int) -> Order:
        if self._get_quantity_of_item(order_id, item_id) == 1:
            self.db_connector.sql_query()
        else:
            self.db_connector.sql_query()

    def _get_quantity_of_item(self, item_id: int, order_id: int) -> int:
        result = self.db_connector.sql_query(
            """SELECT item_quantity
               FROM Order_Items
               WHERE order_id=%(order_is)s AND item_id=%(item_id)s;
            """,
            {"item_id": item_id, "order_id": order_id},
            "one",
        )
        if result is not None:
            return result["item_quantity"]

        return 0
