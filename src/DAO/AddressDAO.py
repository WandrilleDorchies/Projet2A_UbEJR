from typing import Optional

from src.Model.Address import Address
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class AddressDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_address(self, customer_id) -> Optional[Address]:
        """
        Retrieve the address associated with a given customer.

        Args
        ----
        customer_id (int):
            Unique identifier of the customer whose address is requested.

        Returns
        -------
        Address or None
            An Address object containing the customer's address information
            if found in the database, None otherwise.
        """

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
        """
        Retrieve all addresses stored in the database.

        Returns
        -------
        list[Address] or None
            A list of Address objects if at least one address exists in the database,
            None otherwise.
        """

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
        """
        Create a new address entry in the database.

        Args
        ----
        address_id (int):
            Unique identifier for the address (ignored in insertion since set to DEFAULT).
        number (str or int):
            Street number of the address.
        street (str):
            Name of the street.
        city (str):
            City where the address is located.
        postal_code (str or int):
            Postal code of the address.
        country (str):
            Country of the address.

        Returns
        -------
        Address
            The newly created Address object containing the inserted information.
        """

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
        """
        Update an existing address in the database.

        Args
        ----
        address_id (int):
            Unique identifier of the address to update.
        number (str or int):
            Updated street number of the address.
        street (str):
            Updated street name.
        city (str):
            Updated city name.
        postal_code (str or int):
            Updated postal code.
        country (str):
            Updated country name.

        Returns
        -------
        Address
            The updated Address object reflecting the new information stored in the database.
        """

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
        """
        Delete the address associated with a given customer from the database.

        Args
        ----
        customer_id (int):
            Unique identifier of the customer whose address should be deleted.

        Returns
        -------
        Address or None
            The deleted Address object if the operation was successful, None otherwise.
        """

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
