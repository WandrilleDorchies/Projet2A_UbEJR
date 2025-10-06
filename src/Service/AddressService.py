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
        self, number: int, street: str, city: str, postal_code: int, country: str
    ) -> None:
        address: str = f"{number} {street}, {postal_code} {city}, {country}"

        if self.is_valid(address):
            self.dao.create_address(number, street, city, postal_code, country)

    def update_adress(
        self,
        number: int = None,
        street: str = None,
        city: str = None,
        postal_code: int = None,
        country: str = None,
    ) -> None:
        pass
