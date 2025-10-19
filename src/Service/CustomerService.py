from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Address import Address
from src.Service.GoogleMapService import GoogleMapService

from .UserService import UserService


class CustomerService:
    def __init__(
        self, user_service: UserService, customer_dao: CustomerDAO, gm_service: GoogleMapService
    ):
        self.user_service = user_service
        self.customer_dao = customer_dao
        self.gm_service = gm_service

    def create_customer(
        self,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        phone: str,
        mail: str,
    ):
        hashed_password: str = self.user_service.create_hashed_password(password)
        customer_address = self.gm_service.validate_address(address)
        address_id = customer

        return self.customer_dao.create_customer(
            first_name, last_name, phone, mail, hashed_password, address_id
        )

    def update_customer():
        pass

    def delete_customer():
        pass

    def get_customer_by_id():
        pass
