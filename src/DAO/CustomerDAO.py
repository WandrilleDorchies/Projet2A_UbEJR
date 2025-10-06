from typing import Optional

from src.Model.Customer import Customer
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class CustomerDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_customer_by_id(self, customer_id) -> Optional[Customer]:
        raw_customer = self.db_connector.sql_query(
            "SELECT * from Customers WHERE id=%s", [customer_id], "one"
        )
        if raw_customer is None:
            return None
        # pyrefly: ignore
        return Customer(**raw_customer)

    def get_all_customer(self) -> Optional[list[Customer]]:
        raw_customers = self.db_connector.sql_query("SELECT * from Customers ", "all")

        if raw_customers is None:
            return None

        list_customer = [Customer(**customer) for customer in raw_customers]
        return list_customer

    def create_customer(
        self, customer_id, first_name, last_name, phone, mail, password_hash, address_id
    ) -> Customer:
        raw_created_customer = self.db_connector.sql_query(
            """
        INSERT INTO Address (customer_id, first_name, last_name, phone, mail, password_hash, address_id)
        VALUES (DEFAULT, %(first_name)s,%(last_name)s, %(phone)s, %(mail)s, %(password_hash)s, %(address_id)s )
        RETURNING *;
        """,
        )
        return Customer(**raw_created_customer)

    def update_customer(
        self, customer_id, first_name, last_name, phone, mail, password_hash, address_id
    ):
        raw_update_customer = self.db_connector.sql_query(
            """
        UPDATE Address SET first_name = %(first_name)s, last_name=%(last_name)s, phone=%(phone)s, mail=%(mail)s,
        password_hash=%(password_hash)s, address_id=%(address_id)s
        WHERE customer_id=%(customer_id)s RETURNING *;
        """,
            {"key": 1},
            "one",
        )
        return Customer(**raw_update_customer)

    def delete_customer(self, customer_id):
        raw_delete_customer = self.db_connector.sql_query(
            """
        DELETE FROM Customers WHERE customer_id=%s
        """,
            "one",
        )
        return Customer(**raw_delete_customer)
