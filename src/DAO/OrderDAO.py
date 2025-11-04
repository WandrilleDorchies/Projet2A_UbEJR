from datetime import datetime
from typing import Dict, List, Optional, Union

from src.Model.Bundle import Bundle
from src.Model.Item import Item
from src.Model.Order import Order
from src.utils.log_decorator import log
from src.utils.singleton import Singleton

from .BundleDAO import BundleDAO
from .DBConnector import DBConnector
from .ItemDAO import ItemDAO
from .OrderableDAO import OrderableDAO


class OrderDAO(metaclass=Singleton):
    db_connector: DBConnector
    orderable_dao: OrderableDAO
    item_dao: ItemDAO
    bundle_dao: BundleDAO

    def __init__(
        self,
        db_connector: DBConnector,
        orderable_dao: OrderableDAO,
        item_dao: ItemDAO,
        bundle_dao: BundleDAO,
    ) -> None:
        self.db_connector = db_connector
        self.orderable_dao = orderable_dao
        self.item_dao = item_dao
        self.bundle_dao = bundle_dao

    # CREATE
    @log
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

        raw_order["order_orderables"] = {}
        return Order(**raw_order)

    # READ
    @log
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

        raw_order["order_orderables"] = self._get_orderables_in_order(order_id)
        return Order(**raw_order)

    @log
    def get_all_orders(self) -> Optional[List[Order]]:
        raw_orders = self.db_connector.sql_query("SELECT * from Orders", return_type="all")

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    @log
    def get_all_orders_by_customer(self, customer_id: int) -> Optional[List[Order]]:
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Orders where order_customer_id=%s", [customer_id], "all"
        )

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    @log
    def get_customer_current_order(self, customer_id: int) -> Optional[Order]:
        raw_order = self.db_connector.sql_query(
            "SELECT * from Orders WHERE order_customer_id=%s AND order_state != 2",
            [customer_id],
            "one",
        )
        if raw_order is None:
            return None

        raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
        return Order(**raw_order)

    @log
    def get_paid_orders(self) -> Optional[List[Order]]:
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Orders WHERE order_is_paid is True", return_type="all"
        )

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    @log
    def get_prepared_orders(self) -> Optional[List[Order]]:
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Orders WHERE order_is_prepared is True", return_type="all"
        )

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    @log
    def get_current_orders(self):
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Orders WHERE order_state IN (0, 1)", return_type="all"
        )

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    @log
    def get_available_orders(self):
        raw_orders = self.db_connector.sql_query(
            """SELECT * from Orders
            WHERE order_state = 0
                  AND order_is_prepared=True
                  AND order_is_prepared=True;""",
            return_type="all",
        )

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    @log
    def get_past_orders(self):
        raw_orders = self.db_connector.sql_query(
            "SELECT * from Orders WHERE order_state = 2", return_type="all"
        )

        if not raw_orders:
            return []

        Orders = []
        for raw_order in raw_orders:
            raw_order["order_orderables"] = self._get_orderables_in_order(raw_order["order_id"])
            Orders.append(Order(**raw_order))

        return Orders

    # UPDATE
    @log
    def update_order(self, order_id: int, update: dict) -> Order:
        if not update:
            raise ValueError("At least one value should be updated")

        for key in update.keys():
            if key not in ["order_is_paid", "order_is_prepared", "order_state"]:
                raise ValueError(f"{key} is not a parameter of Order.")
        if update.get("order_state") and update["order_state"] not in (0, 1, 2):
            raise ValueError("State can only take 1, 2 or 3 as value.")

        updated_fields = [f"{field} = %({field})s" for field in update.keys()]
        set_field = ", ".join(updated_fields)
        params = {**update, "order_id": order_id}

        self.db_connector.sql_query(
            f"""
            UPDATE Orders
            SET {set_field}
            WHERE order_id = %(order_id)s;
            """,
            params,
            "none",
        )

        return self.get_order_by_id(order_id)

    # DELETE
    @log
    def delete_order(self, order_id) -> None:
        self.db_connector.sql_query(
            """
            DELETE FROM Order_contents WHERE order_id=%s;
            """,
            [order_id],
            "none",
        )
        self.db_connector.sql_query(
            """
            DELETE FROM Orders WHERE order_id=%s;
            """,
            [order_id],
            "none",
        )
        return None

    @log
    def add_orderable_to_order(self, order_id: int, orderable_id: int, quantity: int = 1) -> Order:
        if self._get_quantity_of_orderables(order_id, orderable_id) >= 1:
            self.db_connector.sql_query(
                """UPDATE Order_contents
                   SET orderable_quantity=orderable_quantity+%(quantity)s
                   WHERE order_id=%(order_id)s AND orderable_id=%(orderable_id)s;
                """,
                {"quantity": quantity, "order_id": order_id, "orderable_id": orderable_id},
                "none",
            )

        else:
            self.db_connector.sql_query(
                """INSERT INTO Order_contents
                   VALUES (%(order_id)s, %(orderable_id)s, %(quantity)s);
                """,
                {"order_id": order_id, "orderable_id": orderable_id, "quantity": quantity},
                "none",
            )

        return self.get_order_by_id(order_id)

    @log
    def remove_orderable_from_order(
        self, order_id: int, orderable_id: int, quantity: int = 1
    ) -> Order:
        if self._get_quantity_of_orderables(order_id, orderable_id) <= quantity:
            self.db_connector.sql_query(
                """DELETE FROM Order_contents
                   WHERE order_id=%(order_id)s AND orderable_id=%(orderable_id)s;
                """,
                {"order_id": order_id, "orderable_id": orderable_id},
                "none",
            )
        else:
            self.db_connector.sql_query(
                """UPDATE Order_contents
                   SET orderable_quantity=orderable_quantity-%(quantity)s
                   WHERE order_id=%(order_id)s AND orderable_id=%(orderable_id)s;
                """,
                {"quantity": quantity, "order_id": order_id, "orderable_id": orderable_id},
                "none",
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
        if result is None:
            return 0

        return result["orderable_quantity"]

    def _get_orderables_in_order(self, order_id: int) -> Dict[Union[Item, Bundle], int]:
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
            return {}

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
