from typing import Optional

from dao.db_connection import DBConnection

from src.Model.Address import Address

from .DBConnector import DBConnector


class AddressDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_address(self, customer_id) -> Address:
        """Get the Adress of one customer thanks to customer_id"""
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT *        "
                    "FROM Address   "
                    "JOIN Customer                          "
                    "USING address_id                          "
                    "WHERE customer_id = %(customer_id)s                          ",
                    {"customer_id": customer_id},
                )
                address_bdd = cursor.fetchone()

        address = None
        if address_bdd:
            address = Address(
                number=address_bdd["number"],
                street=address_bdd["street"],
                city=address_bdd["city"],
                postal_code=address_bdd["postal_code"],
                country=address_bdd["country"],
            )
        return address

    def get_all_addresses(self) -> list[Address]:
        """Get all addresses"""
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT *                     FROM Address ;                    ")
                address_bdd = cursor.fetchall()

        list_address = []

        if address_bdd:
            for address in address_bdd:
                list_address.append(
                    Address(
                        number=address["number"],
                        street=address["street"],
                        city=address["city"],
                        postal_code=address["postal_code"],
                        country=address["country"],
                    )
                )

        return list_address

        def create_address(self, address_id, number, street, city, postal_code, country)-> bool :
            #TO DO



