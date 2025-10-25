from typing import List, Optional

from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address
from src.utils.log_decorator import log

from .GoogleMapService import GoogleMapService


class AddressService:
    address_dao: AddressDAO

    def __init__(self, address_dao: AddressDAO) -> None:
        self.address_dao = address_dao
        self.service = GoogleMapService()

    @log
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        address = self.dao.get_address(address_id)
        return address

    @log
    def get_address_by_customer_id(self, customer_id: int) -> Optional[Address]:
        address = self.dao.get_address_by_customer_id(customer_id)
        return address

    @log
    def get_all_address(self) -> Optional[List[Address]]:
        addresses = self.dao.get_all_address()
        return addresses

    @log
    def is_valid(self, adress: str) -> bool:
        res: bool = self.service.validate_adress(adress)
        return True if res else False

    @log
    def create_address(
        self,
        address_number: int,
        address_street: str,
        address_city: str,
        address_postal_code: int,
        address_country: str,
    ) -> Optional[Address]:
        address: str = (
            f"{address_number} {address_street},"
            f"{address_postal_code} {address_city}, {address_country}"
        )
        # Est-ce que c'est au service de faire ça ? ou au controller ?

        if self.is_valid(address):
            self.dao.create_address(
                address_number, address_street, address_city, address_postal_code, address_country
            )

    @log
    def update_address(self, address_id: int, update: dict) -> Optional[Address]:
        update_message_parts = []
        for field, value in update.address():
            update_message_parts.append(f"{field}={value}")

        updated_address = self.address_dao.update_address(address_id=id, update=update)
        return updated_address

    @log
    def delete_address(self, address_id: int) -> None:
        address = self.address_dao.get_address_by_id(address_id)
        if address is None:
            raise ValueError(
                f"[AddressService] Cannot delete: address with ID {address_id} not found."
            )

        self.address_dao.delete_address_by_id(address_id)
