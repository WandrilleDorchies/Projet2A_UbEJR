from typing import Optional

from src.Model.Address import Address
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class AddressDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """
        Retrieve the address associated with a given id.

        Args
        ----
        address_id (int):
            Unique identifier of the adress

        Returns
        -------
        Address or None
            An Address object containing the customer's address information
        """

        raw_address = self.db_connector.sql_query(
            """SELECT *
               FROM Addresses
               WHERE address_id = %s;
            """,
            [address_id],
            "one",
        )

        return Address(**raw_address) if raw_address else None

    def get_address_by_customer_id(self, customer_id: int) -> Optional[Address]:
        """
        Retrieve the address associated with a given customer id.

        Args
        ----
        customer_id (int):
            Unique identifier of the customer

        Returns
        -------
        Address or None
            An Address object containing the customer's address information
        """

        raw_address = self.db_connector.sql_query(
            """SELECT a.*
               FROM Addresses AS a
               INNER JOIN Customers AS c ON a.address_id=c.customer_address_id
               WHERE address_id = %s;
            """,
            [customer_id],
            "one",
        )

        return Address(**raw_address) if raw_address else None

    def get_all_addresses(self) -> Optional[list[Address]]:
        """
        Retrieve all addresses stored in the database.

        Returns
        -------
        list[Address] or None
            A list of Address objects if at least one address exists in the database,
            None otherwise.
        """

        raw_addresses = self.db_connector.sql_query("SELECT * FROM Addresses", return_type="all")

        return [Address(**raw_address) for raw_address in raw_addresses] if raw_addresses else None

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
            INSERT INTO Addresses (address_id, address_number, address_street, address_city,
            address_postal_code, address_country)
            VALUES (DEFAULT, %(number)s, %(street)s, %(city)s, %(postal_code)s, %(country)s)
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
        print(raw_created_address)
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

        parameters_update = [
            "address_number",
            "address_street",
            "address_city",
            "address_postal_code",
            "address_country",
        ]
        for key in update.keys():
            if key not in parameters_update:
                raise ValueError(f"{key} is not a parameter of Address.")

        updated_fields = [f"{field} = %({field})s" for field in update.keys()]
        set_field = ", ".join(updated_fields)
        params = {**update, "address_id": address_id}

        self.db_connector.sql_query(
            f"""
            UPDATE Addresses
            SET {set_field}
            WHERE address_id = %(address_id)s;
            """,
            params,
            "none",
        )

        return self.get_address_by_id(address_id)

    def delete_address_by_id(self, address_id: int) -> None:
        self.db_connector.sql_query(
            "DELETE FROM Addresses WHERE address_id = %(address_id)s",
            {"address_id": address_id},
            None,
        )
