from typing import Optional

from src.Model.Address import Address

from .DBConnector import DBConnector


class AddressDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_address(self, customer_id) -> Optional[Address]:
        """Get the Adress of one customer thanks to customer_id"""
        raw_address = self.db_connector.sql_query(
            "SELECT *        "
            "FROM Address   "
            "JOIN Customer                          "
            "USING address_id                          "
            "WHERE customer_id = %(customer_id)s                          ",
            {"customer_id": customer_id},
            "one",
        )
        if raw_address:
            raw_address = Address(
                number=raw_address["number"],
                street=raw_address["street"],
                city=raw_address["city"],
                postal_code=raw_address["postal_code"],
                country=raw_address["country"],
            )
        return raw_address

    def get_all_addresses(self) -> Optional[list[Address]]:
        """Get all addresses"""
        address_bdd = self.db_connector.sql_query("SELECT * FROM Address", "all")

        list_address = []

        if address_bdd is None:
            return None

        list_address = [
            Address(
                number=address["number"],
                street=address["street"],
                city=address["city"],
                postal_code=address["postal_code"],
                country=address["country"],
            )
            for address in address_bdd
        ]
        return list_address

    def create_address(self, address_id, number, street, city, postal_code, country) -> Address:
        raw_created_address = self.db_connector.sql_query(
            """
        INSERT INTO Address (address_id, number, street, city, postal_code, country)
        VALUES (DEFAULT, %(number)s,%(street)s, %(city)s, %(postal_code)s, %(country)s)
        RETURNING *;
        """,
            {"key": 1},
            "one",
        )
        return Address(**raw_created_address)

    def update_address(self, address_id, number, street, city, postal_code, country):
        raw_update_address = self.db_connector.sql_query(
            """
        UPDATE Address SET number = %(number)s, street=%(street)s, city=%(city)s,
        postal_code=%(postal_code)s, country=%(country)s
        WHERE address_id=%(address_id)s RETURNING *;
        """,
            {"key": 1},
            "one",
        )
        return Address(**raw_update_address)

    def delete_address_by_customer(self, customer_id):
        raw_delete_address = self.db_connector.sql_query(
            """
        DELETE FROM Address JOIN Customers Using (address_id) WHERE customer_id=%s
        """,
            "one",
        )
        if raw_delete_address:
            raw_delete_address = Address(
                number=raw_delete_address["number"],
                street=raw_delete_address["street"],
                city=raw_delete_address["city"],
                postal_code=raw_delete_address["postal_code"],
                country=raw_delete_address["country"],
            )
        return raw_delete_address
