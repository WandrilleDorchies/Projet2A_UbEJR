from typing import Optional

from src.Model.Customer import Customer

from .DBConnector import DBConnector


class CustomerDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_customer_by_id(self, customer_id):
        raw_customer = self.db_connector.sql_query("SELECT * from Customers WHERE id=%s", [customer_id], "one")
        if raw_customer is None:
            return None
        # pyrefly: ignore
        return Customer(**raw_customer)
