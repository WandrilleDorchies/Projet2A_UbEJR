from typing import List, Optional

from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Address import Address
from src.Model.Customer import Customer
from src.Model.Order import Order
from src.Service.GoogleMapService import GoogleMapService
from src.utils.log_decorateur import log

from .UserService import UserService


class CustomerService:
    customer_dao: CustomerDAO
    order_dao: OrderDAO

    def __init__(
        self,
        user_service: UserService,
        customer_dao: CustomerDAO,
        order_dao: OrderDAO,
        gm_service: GoogleMapService,
    ):
        self.user_service = user_service
        self.customer_dao = customer_dao
        self.order_dao = order_dao
        self.gm_service = gm_service

    @log
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        customer = self.customer_dao.get_customer_by_id(customer_id)
        return customer

    @log
    def get_customer_by_email(self, customer_email: int) -> Optional[Customer]:
        customer = self.customer_dao.get_customer_by_email(customer_email)
        return customer

    @log
    def get_all_customer(self) -> Optional[List[Customer]]:
        customers = self.customer_dao.get_all_customer()
        return customers

    @log
    def get_all_customer_email(self) -> Optional[List[str]]:
        customers_email = self.customer_dao.get_all_customer_email()
        return customers_email

    @log
    def create_customer(
        self,
        password: str,
        first_name: str,
        last_name: str,
        address: Address,
        phone: str,
        mail: str,
    ) -> Optional[Customer]:

        hashed_password: str = self.user_service.create_hashed_password(password)
        customer_address = self.gm_service.validate_address(address)
        address_id = customer_address.address_id

        created_customer = self.customer_dao.create_customer(
            first_name,
            last_name,
            phone,
            mail,
            hashed_password,
            address_id
        )

        return created_customer

    @log
    def update_customer(self, customer_id: int, update) -> Optional[Customer]:
        update_message_parts = []
        for field, value in update.customer():
            update_message_parts.append(f"{field}={value}")

        updated_customer = self.customer_dao.update_customer(customer_id=customer_id, update=update)
        return updated_customer

    @log
    def order_history(self, customer_id: int) -> Optional[List[Order]]:
        history = self.order_dao.get_all_order_by_customer(customer_id)
        return history

    @log
    def make_order() -> Order:
        # TODO
        pass

    @log
    def delete_customer(self, customer_id: int) -> None:
        """
        Deletes a customer from the database by its ID.

        Parameters
        ----------
        customer_id : int
            The ID of the customer to delete.
        """
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError(
                f"[CustomerService] Cannot delete: customer with ID {customer_id} not found."
            )

        self.customer_dao.delete_customer_by_id(customer_id)


