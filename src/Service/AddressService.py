from typing import List, Optional

from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address
from src.utils.log_decorator import log

from .GoogleMapService import GoogleMapService


class AddressService:
    address_dao: AddressDAO
    gm_service: GoogleMapService

    def __init__(self, address_dao: AddressDAO, gm_service: GoogleMapService) -> None:
        self.address_dao = address_dao
        self.gm_service = gm_service

    @log
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        address = self.address_dao.get_address_by_id(address_id)
        if address is None:
            raise ValueError(
                f"[AddressService]: Cannot find: Addres with ID {address_id} not found."
            )
        return address

    @log
    def get_address_by_customer_id(self, customer_id: int) -> Optional[Address]:
        address = self.address_dao.get_address_by_customer_id(customer_id)
        return address

    @log
    def get_all_address(self) -> Optional[List[Address]]:
        addresses = self.address_dao.get_all_address()
        return addresses

    @log
    def create_address(
        self,
        address: str,
    ) -> Optional[Address]:
        self.gm_service.validate_address(address)

        components = self.gm_service.extract_components(address)
        return self.address_dao.create_address(**components)

    @log
    def update_address(self, address_id: int, update: dict) -> Optional[Address]:
        current_address = self.get_address_by_id(address_id)

        if all([value is None for value in update.values()]):
            raise ValueError(
                "[AddressService] Cannot update address: You must change at least one field."
            )

        for key, value in update.items():
            if not value:
                update[key] = getattr(current_address, key)

        address = (
            f"{update['address_number']} {update['address_street']},"
            f"{update['address_postal_code']} {update['address_city']}, {update['address_country']}"
        )
        self.gm_service.validate_address(address)
        components = self.gm_service.extract_components(address)
        return self.address_dao.update_address(address_id, components)

    @log
    def delete_address(self, address_id: int) -> None:
        self.get_address_by_id(address_id)
        self.address_dao.delete_address_by_id(address_id)
