from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address

from .GoogleMapService import GoogleMapService


class AddressService:
    def __init__(self) -> None:
        self.dao = AddressDAO()
        self.service = GoogleMapService()

    def get_adress_by_user(self, user_id: int) -> Address:
        adress = self.dao.get_address(user_id)
        return adress

    def is_valid(self, adress: Address) -> bool:
        res: bool = self.service.validate_adress(adress)
        return res

    def create_adress(self, number, street, city, postal_code, country) -> None:
        self.dao.create_address()

    def update_adress(self) -> None:
        pass
