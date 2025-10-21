from datetime import datetime
from typing import Dict, List, Optional

from src.Model.Item import Item
from src.Model.Order import Order
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class OrderDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        raw_order = self.db_connector.sql_query(
            """SELECT *
               FROM Orders
               WHERE order_id=%s""",
            [order_id],
            "one",
        )

        if raw_order is None:
            return None

        raw_order["order_items"] = self._get_items_in_order(order_id)
        return Order(**raw_order)

    def get_all_orders(self) -> Optional[List[Order]]:
        raw_orders = self.db_connector.sql_query("SELECT * from Orders", [], "all")

        if not raw_orders:
            return None

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_items"] = self._get_items_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    def create_order(self, customer_id: int) -> Order:
        raw_order = self.db_connector.sql_query(
            """
            INSERT INTO Orders (order_id,
                               order_customer_id,
                               order_state,
                               order_date,
                               order_time,
                               order_is_paid,
                               order_is_prepared)
            VALUES (DEFAULT,
                    %(customer_id)s,
                    0,
                    %(order_date)s,
                    %(order_time)s,
                    FALSE,
                    FALSE)
            RETURNING *;
            """,
            {
                "customer_id": customer_id,
                "order_date": datetime.today().strftime('%Y-%m-%d'),
                "order_time": datetime.now(),
            },
            "one",
        )

        raw_order["order_items"] = {}
        return Order(**raw_order)

    def update_order(self, order_id, is_paid, is_prepared) -> Order:
        raw_order = self.db_connector.sql_query(
            """
            UPDATE Orders SET order_is_paid=%(is_paid)s, order_is_prepared=%(is_prepared)s
            WHERE order_id=%(order_id)s RETURNING *;
            """,
            {"is_paid": is_paid, "is_prepared": is_prepared, "order_id": order_id},
            "one",
        )
        raw_order["order_items"] = self._get_items_in_order(order_id)
        return Order(**raw_order)

    def delete_order(self, order_id) -> None:
        self.db_connector.sql_query(
            """
            DELETE FROM Orders WHERE order_id=%s;
            """,
            [order_id],
            "none",
        )
        self.db_connector.sql_query(
            """
            DELETE FROM Order_Items WHERE order_id=%s;
            """,
            [order_id],
            "none",
        )

        return None

    def add_item_to_order(self, item_id: int, order_id: int) -> Order:
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
                   VALUES (%(order_id)s, %(item_id)s, 1);
                """,
                {"order_id": order_id, "item_id": item_id},
                "one",
            )

        return self.get_order_by_id(order_id)

    def remove_item_from_order(self, order_id: int, item_id: int) -> Order:
        if self._get_quantity_of_item(order_id, item_id) == 1:
            self.db_connector.sql_query(
                """DELETE FROM Order_Items
                   WHERE order_id=%(order_id)s AND item_id=%(item_id)s;
                """,
                {"order_id": order_id, "item_id": item_id},
                "one",
            )
        else:
            self.db_connector.sql_query(
                """UPDATE Order_Items
                   SET item_quantity=item_quantity-1
                   WHERE order_id=%(order_id)s AND item_id=%(item_id)s;
                """,
                {"order_id": order_id, "item_id": item_id},
                "one",
            )

        return self.get_order_by_id(order_id)

    def _get_quantity_of_item(self, order_id: int, item_id: int) -> int:
        result = self.db_connector.sql_query(
            """SELECT item_quantity
               FROM Order_Items
               WHERE order_id=%(order_id)s AND item_id=%(item_id)s;
            """,
            {"item_id": item_id, "order_id": order_id},
            "one",
        )
        if result is not None:
            return result["item_quantity"]

        return 0

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
