from typing import Optional

from src.Model.Address import Address
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class AddressDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_address(self, customer_id: int) -> Optional[Address]:
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
            """SELECT a.* FROM Addresses a
               JOIN Customers c ON a.address_id = c.customer_address_id
               WHERE c.customer_id = %(customer_id)s""",
            [customer_id],
            "one",
        )
        if raw_address is None:
            return None
        return Address(**raw_address)

    def get_all_addresses(self) -> Optional[list[Address]]:
        """
        Retrieve all addresses stored in the database.

        Returns
        -------
        list[Address] or None
            A list of Address objects if at least one address exists in the database,
            None otherwise.
        """

        raw_addresses = self.db_connector.sql_query("SELECT * FROM Address", "all")

        if raw_addresses is None:
            return None

        addresses = [Address(**raw_address) for raw_address in raw_addresses]

        return addresses

    def create_address(
        self, number: int, street: str, city: str, postal_code: int, country: str
    ) -> Address:
        """
        Create a new address entry in the database.

        Args
        ----
        address_number (str or int):
            Street number of the address.
        address_street (str):
            Name of the street.
        address_city (str):
            City where the address is located.
        address_postal_code (str or int):
            Postal code of the address.
        address_country (str):
            Country of the address.

        Returns
        -------
        Address
            The newly created Address object containing the inserted information.
        """

        raw_created_address = self.db_connector.sql_query(
            """
        INSERT INTO Address (address_id, address_number, address_street, address_city,
        address_postal_code, address_country)
        VALUES (DEFAULT, %(number)s, '%(street)s', '%(city)s', %(postal_code)s, '%(country)s')
        RETURNING *;
        """,
            {
                "number": number,
                "street": street,
                "city": city,
                "postal_code": postal_code,
                "country": country,
            },
            "one",
        )
        return Address(**raw_created_address)

    def update_address(self, address_id: int, update: dict):
        """
        Update an existing address in the database.

        Args
        ----
        address_id (int):
            Unique identifier of the address to update.
        ? (str or int):
            ?.

        Returns
        -------
        Address
            The updated Address object reflecting the new information stored in the database.
        """

        if not update:
            raise ValueError("At least one value should be updated")

        updated_fields = []
        for field in update.keys():
            updated_fields.append(f"{field} = %({field})s")

        params = {"address_id": address_id}
        for field_name, value in update.address():
            params[field_name] = value

        raw_update_address = self.db_connector.sql_query(
            f"""
        UPDATE Adresses SET {", ".join(updated_fields)}
        WHERE address_id = %(address_id)s RETURNING *;
        """,
            params,
            "one",
        )

        return Address(**raw_update_address)
