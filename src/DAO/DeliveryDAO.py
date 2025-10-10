from typing import Optional

from src.Model.Delivery import Delivery
from src.Model.order import Order
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class DeliveryDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

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

    def get_delivery_by_driver(self, delivery_id_driver: int) -> Optional[Order]:
        raw_delivery = self.db_connector.sql_query(
            "SELECT * from Deliveries WHERE delivery_id_driver=%s", [delivery_id_driver], "one"
        )
        if raw_delivery is None:
            return None
        # pyrefly: ignore
        return Delivery(**raw_delivery)

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
        # pyrefly: ignore
        return Delivery(**raw_delivery)

    def update_delivery(self, delivery_id, state) -> Delivery:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_update_delivery = self.db_connector.sql_query(
            """
        UPDATE Deliveries SET delivery_state=%(state)s
        WHERE delivery_id_order=%(delivery_id)s RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 1},
            "one",
        )
        # pyrefly: ignore

        return Delivery(**raw_update_delivery)

    def delete_delivery(self, delivery_id) -> None:
        # TODO: decide return type
        #     : handle autonumber & check for existing item with similar name
        raw_delete_delivery = self.db_connector.sql_query(
            """
        DELETE FROM Deliveries WHERE delivery_id_order=%s RETURNING *;
        """,
            # TODO: dic with column and values
            {"key": 1},
            "one",
        )
        # pyrefly: ignore

        return Delivery(**raw_delete_delivery)
