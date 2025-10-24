from typing import Optional

from src.Model.Delivery import Delivery
from src.Model.order import Order
from src.utils.log_decorator import log
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class DeliveryDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    @log
    def create_delivery(self, order_id: int, driver_id: int) -> Delivery:
        raw_created_delivery = self.db_connector.sql_query(
            """
        INSERT INTO Delivery (order_id, driver_id, delivery_state)
        VALUES (%(order_id)s, %(driver_id)s, DEFAULT)
        RETURNING *;
        """,
            {"order_id": order_id, "driver_id": driver_id},
            "one",
        )

        return Delivery(**raw_created_delivery)

    @log
    def get_delivery_by_driver(self, delivery_id_driver: int) -> Optional[Order]:
        raw_delivery = self.db_connector.sql_query(
            "SELECT * from Deliveries WHERE delivery_id_driver=%s", [delivery_id_driver], "one"
        )
        if raw_delivery is None:
            return None
        return Delivery(**raw_delivery)

    @log
    def get_delivery_by_user(self, customer_id: int) -> Optional[Order]:
        raw_delivery = self.db_connector.sql_query(
            """SELECT * from Deliveries
            LEFT JOIN Order ON Deliveries.delivery_id_order = Order.order_id
            WHERE order_customer_id=%s""",
            [customer_id],
            "one",
        )
        if raw_delivery is None:
            return None
        return Delivery(**raw_delivery)

    @log
    def update_delivery_state(self, delivery_id: int, state: int) -> Delivery:
        if state not in [0, 1, 2]:
            raise ValueError("State can only take 1, 2 or 3 as value.")
        raw_update_delivery = self.db_connector.sql_query(
            """
            UPDATE Deliveries SET delivery_state=%(state)s
            WHERE delivery_id_order=%(delivery_id)s RETURNING *;
            """,
            {"state": state, "delivery_id": delivery_id},
            "one",
        )
        return Delivery(**raw_update_delivery)

    @log
    def change_driver(self, delivery_id: int, driver_id: int) -> Delivery:
        raw_update_delivery = self.db_connector.sql_query(
            """
            UPDATE Deliveries SET driver_id=%(driver_id)s
            WHERE delivery_id_order=%(delivery_id)s RETURNING *;
            """,
            {"driver_id": driver_id, "delivery_id": delivery_id},
            "one",
        )
        return Delivery(**raw_update_delivery)

    @log
    def delete_delivery(self, delivery_id: int) -> None:
        raw_delete_delivery = self.db_connector.sql_query(
            """
            DELETE FROM Deliveries WHERE delivery_id_order=%s RETURNING *;
            """,
            [delivery_id],
            "one",
        )
        return Delivery(**raw_delete_delivery)
