from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address

from .GoogleMapService import GoogleMapService


class AddressService:
    def __init__(self) -> None:
        self.dao = AddressDAO()
        self.service = GoogleMapService()

    def get_address_by_user(self, user_id: int) -> Address:
        adress = self.dao.get_address(user_id)
        return adress

    def is_valid(self, adress: str) -> bool:
        res: bool = self.service.validate_adress(adress)
        return True if res else False

    def create_address(
        self,
        address_number: int,
        address_street: str,
        address_city: str,
        address_postal_code: int,
        address_country: str,
    ) -> None:
        address: str = f"{address_number} {address_street}, {address_postal_code} {address_city}, {address_country}"

        if self.is_valid(address):
            self.dao.create_address(
                address_number, address_street, address_city, address_postal_code, address_country
            )

    def update_address(self, update: dict) -> None:
        update_message_parts = []
        for field, value in update.address():
            update_message_parts.append(f"{field}={value}")

        print(f"[AddressService] Updating address: {', '.join(update_message_parts)}")

        updated_address = self.address_dao.update_address(address_id=id, update=update)
        print(f"[AddressService] DAO returned after creation: {updated_address}")
        return updated_address

    def delete_address(self, address_id: int) -> None:
        """
        Deletes an address from the database by its ID.

        Parameters
        ----------
        address_id : int
            The ID of the address to delete.
        """
        print(f"[AddressService] Deleting address with ID: {address_id}")

        address = self.address_dao.get_address_by_id(address_id)
        if address is None:
            raise ValueError(
                f"[AddressService] Cannot delete: address with ID {address_id} not found."
            )

        self.address_dao.delete_address_by_id(address_id)
        print(f"[AddressService] Address with ID {address_id} has been deleted.")
