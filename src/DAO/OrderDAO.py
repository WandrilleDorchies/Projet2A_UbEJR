from datetime import datetime
from typing import Dict, List, Optional

from src.Model.Bundle import Bundle
from src.Model.Item import Item
from src.Model.Order import Order
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class OrderDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    # CREATE
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
                "order_date": datetime.today().strftime("%Y-%m-%d"),
                "order_time": datetime.now(),
            },
            "one",
        )

        raw_order["order_items"] = {}
        return Order(**raw_order)

    # READ
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

        raw_order["order_items"] = self._get_orderables_in_order(order_id)
        return Order(**raw_order)

    def get_all_orders(self) -> Optional[List[Order]]:
        raw_orders = self.db_connector.sql_query("SELECT * from Orders", return_type="all")

        if not raw_orders:
            return None

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_items"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    # UPDATE
    def update_order(self, order_id, is_paid, is_prepared) -> Order:
        raw_order = self.db_connector.sql_query(
            """
            UPDATE Orders SET order_is_paid=%(is_paid)s, order_is_prepared=%(is_prepared)s
            WHERE order_id=%(order_id)s RETURNING *;
            """,
            {"is_paid": is_paid, "is_prepared": is_prepared, "order_id": order_id},
            "one",
        )
        raw_order["order_items"] = self._get_orderables_in_order(order_id)
        return Order(**raw_order)

    # DELETE
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
            DELETE FROM Order_contents WHERE order_id=%s;
            """,
            [order_id],
            "none",
        )
        return None

    def add_orderable_to_order(self, orderable_id: int, order_id: int) -> Order:
        if self._get_quantity_of_orderables(orderable_id, order_id) >= 1:
            self.db_connector.sql_query(
                """UPDATE Order_contents
                   SET orderable_quantity=orderable_quantity+1
                   WHERE order_id=%(order_id)s AND item_id=%(orderable_id)s;
                """,
                {"order_id": order_id, "orderable_id": orderable_id},
                "one",
            )

        else:
            self.db_connector.sql_query(
                """INSERT INTO Order_Items
                   VALUES (%(order_id)s, %(orderable_id)s, 1);
                """,
                {"order_id": order_id, "orderable_id": orderable_id},
                "one",
            )

        return self.get_order_by_id(order_id)

    def remove_orderable_from_order(self, order_id: int, orderable_id: int) -> Order:
        if self._get_quantity_of_orderables(order_id, orderable_id) == 1:
            self.db_connector.sql_query(
                """DELETE FROM Order_contents
                   WHERE order_id=%(order_id)s AND orderable_id=%(orderable_id)s;
                """,
                {"order_id": order_id, "orderable_id": orderable_id},
                "one",
            )
        else:
            self.db_connector.sql_query(
                """UPDATE Order_contents
                   SET orderable_quantity=orderable_quantity-1
                   WHERE order_id=%(order_id)s AND orderable_id=%(orderable_id)s;
                """,
                {"order_id": order_id, "orderable_id": orderable_id},
                "one",
            )

        return self.get_order_by_id(order_id)

    def _get_quantity_of_orderables(self, order_id: int, orderable_id: int) -> int:
        result = self.db_connector.sql_query(
            """SELECT orderable_quantity
               FROM Order_contents
               WHERE order_id=%(order_id)s AND orderable_id=%(orderable_id)s;
            """,
            {"order_id": order_id, "orderable_id": orderable_id},
            "one",
        )
        if result is not None:
            return result["item_quantity"]

        return 0

    def _get_orderables_in_order(self, order_id: int) -> Optional[Dict[Item | Bundle, int]]:
        raw_orderables = self.db_connector.sql_query(
            """
            SELECT oc.orderable_id, oc.orderable_quantity, o.orderable_type
            FROM Order_contents AS oc
            JOIN Orderables AS o ON oc.orderable_id = o.orderable_id
            WHERE oc.order_id = %s
            """,
            [order_id],
            "all",
        )
        if not raw_orderables:
            return None

        products_dict = {}
        for raw in raw_orderables:
            orderable_id = raw["orderable_id"]
            quantity = raw["orderable_quantity"]
            orderable_type = raw["orderable_type"]

            if orderable_type == "item":
                product = self.item_dao.get_item_by_orderable_id(orderable_id)
            elif orderable_type == "bundle":
                product = self.bundle_dao.get_bundle_by_orderable_id(orderable_id)

            if product:
                products_dict[product] = quantity

        return products_dict

    def _get_products_in_order(self, order_id: int) -> Dict[Bundle | Item, int]:
        raw_products = self.db_connector.sql_query(
            """
            SELECT op.product_id, op.product_quantity, p.product_type
            FROM Order_Products op
            JOIN Products p ON op.product_id = p.product_id
            WHERE op.order_id = %s
            """,
            [order_id],
            "all",
        )

        products_dict = {}
        for raw in raw_products:
            product_id = raw["product_id"]
            quantity = raw["product_quantity"]
            product_type = raw["product_type"]

            if product_type == "item":
                product = self.item_dao.get_item_by_product_id(product_id)
            elif product_type == "bundle":
                product = self.bundle_dao.get_bundle_by_product_id(product_id)

            if product:
                products_dict[product] = quantity

        return products_dict
