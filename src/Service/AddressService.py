import logging
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
        """
        _summary_

        Parameters
        ----------
        address_id : int
            _description_

        Returns
        -------
        Optional[Address]
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        address = self.address_dao.get_address_by_id(address_id)
        if address is None:
            logging.error(f"[AddressService] Cannot find: Address with ID {address_id} not found.")
            raise ValueError(
                f"[AddressService] Cannot find: Address with ID {address_id} not found."
            )
        return address

    @log
    def get_address_by_customer_id(self, customer_id: int) -> Optional[Address]:
        """
        _summary_

        Parameters
        ----------
        customer_id : int
            _description_

        Returns
        -------
        Optional[Address]
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        address = self.address_dao.get_address_by_customer_id(customer_id)
        if address is None:
            logging.error(
                f"[AddressService] Cannot find Address for customer ID {customer_id} not found."
            )
            raise ValueError(
                f"[AddressService] Cannot find Address for customer ID {customer_id} not found."
            )
        return address

    @log
    def get_all_address(self) -> Optional[List[Address]]:
        """
        _summary_

        Returns
        -------
        Optional[List[Address]]
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        addresses = self.address_dao.get_all_address()
        if addresses is None:
            logging.error("[AddressService] No adresses in the database.")
            raise ValueError("[AddressService] No adresses in the database.")
        return addresses

    @log
    def create_address(
        self,
        address: str,
    ) -> Optional[Address]:
        """
        _summary_

        Parameters
        ----------
        address : str
            _description_

        Returns
        -------
        Optional[Address]
            _description_
        """
        self.gm_service.validate_address(address)

        components = self.gm_service.extract_components(address)
        return self.address_dao.create_address(**components)

    @log
    def update_address(self, address_id: int, update: dict) -> Optional[Address]:
        """
        _summary_

        Parameters
        ----------
        address_id : int
            _description_
        update : dict
            _description_

        Returns
        -------
        Optional[Address]
            _description_

        Raises
        ------
        ValueError
            _description_
        """
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
        """
        _summary_

        Parameters
        ----------
        address_id : int
            _description_
        """
        self.get_address_by_id(address_id)
        self.address_dao.delete_address_by_id(address_id)
