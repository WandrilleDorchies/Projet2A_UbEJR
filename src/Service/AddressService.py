from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address


class AddressService:
    def __init__(
        self,
        addressdao: AddressDAO,
    ):
        self.addressdao = addressdao

    def change_address(self, address: Address, number, street, city, postal_code, country):
        address_id = address.address_id
        updated_address = self.addressdao.update_address(address_id, number, street, city, postal_code, country)
        self.address = updated_address
