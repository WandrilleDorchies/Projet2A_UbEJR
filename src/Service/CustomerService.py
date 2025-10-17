from src.DAO.CustomerDAO import CustomerDAO

from .UserService import UserService


class CustomerService:
    def __init__(self, user_service: UserService, customer_dao: CustomerDAO):
        self.user_service = user_service
        self.customer_dao = customer_dao

    def create_customer():
        pass

    def update_customer():
        pass

    def delete_customer():
        pass

    def get_customer_by_id():
        pass
