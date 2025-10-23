from datetime import datetime
from typing import Optional

from src.Model.Customer import Customer
from src.utils.singleton import Singleton

from .AddressDAO import AddressDAO
from .DBConnector import DBConnector


class CustomerDAO(metaclass=Singleton):
    db_connector: DBConnector
    address_dao: AddressDAO

    def __init__(self, db_connector: DBConnector, address_dao: AddressDAO):
        self.db_connector = db_connector
        self.address_dao = address_dao

    def create_customer(
        self,
        first_name: str,
        last_name: str,
        phone: str,
        mail: str,
        password_hash: str,
        salt: str,
        address_id: int,
    ) -> Customer:
        raw_customer = self.db_connector.sql_query(
            """
            INSERT INTO Customers (customer_id,
                                   customer_first_name,
                                   customer_last_name,
                                   customer_created_at,
                                   customer_phone,
                                   customer_mail,
                                   customer_password_hash,
                                   customer_salt,
                                   customer_address_id)
            VALUES (DEFAULT,
                    %(first_name)s,
                    %(last_name)s,
                    %(customer_created_at)s,
                    %(phone)s,
                    %(mail)s,
                    %(password_hash)s,
                    %(salt)s,
                    %(address_id)s)
            RETURNING *;
            """,
            {
                "first_name": first_name,
                "last_name": last_name,
                "customer_created_at": datetime.now(),
                "phone": phone,
                "mail": mail,
                "password_hash": password_hash,
                "salt": salt,
                "address_id": address_id,
            },
            "one",
        )
        address = self.address_dao.get_address_by_id(raw_customer["customer_address_id"])
        raw_customer["customer_address"] = address
        mapped_args = self._map_db_to_model(raw_customer)
        return Customer(**mapped_args)

    def get_customer_by_id(self, customer_id) -> Optional[Customer]:
        raw_customer = self.db_connector.sql_query(
            "SELECT * from Customers WHERE customer_id=%s", [customer_id], "one"
        )
        if raw_customer is None:
            return None
        mapped_args = self._map_db_to_model(raw_customer)
        return Customer(**mapped_args)

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        raw_customer = self.db_connector.sql_query(
            "SELECT * FROM Customers WHERE customer_email=%s", [email], "one"
        )
        if raw_customer is None:
            return None
        mapped_args = self._map_db_to_model(raw_customer)
        return Customer(**mapped_args)

    def get_all_customer(self) -> Optional[list[Customer]]:
        raw_customers = self.db_connector.sql_query("SELECT * from Customers ", return_type="all")

        if raw_customers is None:
            return None

        list_customer = [Customer(**self._map_db_to_model(customer)) for customer in raw_customers]
        return list_customer

    def update_customer(self, customer_id: int, update: dict):
        if not update:
            raise ValueError("At least one value should be updated")

        parameters_update = [
            "customer_first_name",
            "customer_last_name",
            "customer_password_hash",
            "customer_phone",
            "customer_mail",
        ]
        for key in update.keys():
            if key not in parameters_update:
                raise ValueError(f"{key} is not a parameter of Order.")

        updated_fields = [f"{field} = %({field})s" for field in update.keys()]
        set_field = ", ".join(updated_fields)
        params = {**update, "customer_id": customer_id}

        self.db_connector.sql_query(
            f"""
            UPDATE Customers
            SET {set_field}
            WHERE customer_id = %(customer_id)s;
            """,
            params,
            "none",
        )
        return self.get_customer_by_id(customer_id)

    def delete_customer(self, customer_id: int):
        self.db_connector.sql_query(
            """
            DELETE FROM Customers WHERE customer_id=%s
            """,
            [customer_id],
            "none",
        )

    @staticmethod
    def _map_db_to_model(raw_customer: dict) -> dict:
        """
        Map the column name of the table into the correct name of the arguments
        to build a Customer instance (beacause it inherits from User)
        """
        return {
            "id": raw_customer["customer_id"],
            "first_name": raw_customer["customer_first_name"],
            "last_name": raw_customer["customer_last_name"],
            "password": raw_customer["customer_password_hash"],
            "salt": raw_customer["customer_salt"],
            "created_at": raw_customer["customer_created_at"],
            "customer_phone": raw_customer["customer_phone"],
            "customer_mail": raw_customer["customer_mail"],
            "customer_address": raw_customer["customer_address"],
        }
