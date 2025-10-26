from typing import List, Optional

from Service.PasswordService import check_password_strength, create_salt, hash_password
from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Address import Address
from src.Model.AddressDAP import AddressDAO
from src.Model.Customer import Customer
from src.Model.Order import Order
from src.Service.GoogleMapService import GoogleMapService
from src.utils.log_decorateur import log


class CustomerService:
    customer_dao: CustomerDAO
    order_dao: OrderDAO
    address_dao: AddressDAO
    gm_service: GoogleMapService

    def __init__(
        self,
        customer_dao: CustomerDAO,
        order_dao: OrderDAO,
        address_dao: AddressDAO,
        gm_service: GoogleMapService,
    ):
        self.customer_dao = customer_dao
        self.order_dao = order_dao
        self.address_dao = address_dao
        self.gm_service = gm_service

    @log
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError(
                f"[CustomerService] Cannot find: customer with ID {customer_id} not found."
            )
        return customer

    @log
    def get_customer_by_email(self, customer_email: int) -> Optional[Customer]:
        customer = self.customer_dao.get_customer_by_email(customer_email)
        if customer is None:
            raise ValueError(
                f"[CustomerService] Cannot find: customer with email {customer_email} not found."
            )
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
        first_name: str,
        last_name: str,
        phone: str,
        mail: str,
        password: str,
        address_string: str,
    ) -> Optional[Customer]:
        existing_user = self.customer_dao.get_customer_by_email(mail)
        if existing_user is not None:
            raise ValueError(
                f"[CustomerService] Cannot create: customer with ID {mail} already exists."
            )

        check_password_strength(password)

        address = self.gm_service.validate_address(address_string)
        if address is None:
            raise ValueError(
                "[CustomerService] Cannot create: customer address"
                "is invalid or outside the delivery zone."
            )

        salt = create_salt()
        password_hash = hash_password(password, salt)

        customer = self.customer_dao.create_customer(
            first_name, last_name, phone, mail, password_hash, salt, address.address_id
        )

        return customer

    @log
    def login_customer(self, email: str, password: str) -> Optional[Customer]:
        customer = self.get_customer_by_email(email)
        hashed_password = hash_password(password, customer.salt)

        if hashed_password != customer.password:
            raise ValueError("[CustomerService] Cannot login: customer password is incorrect.")

        return customer

    @log
    def update_customer(self, customer_id: int, update: dict) -> Customer:
        updated_customer = self.customer_dao.update_customer(customer_id=customer_id, update=update)
        return updated_customer

    @log
    def update_address(self, customer_id: int, update: dict) -> Customer:
        self.get_customer_by_id(customer_id)
        current_address = self.address_dao.get_address_by_customer_id(customer_id)
        current_attributes = current_address.get_attributes()

        for key, value in current_attributes.items():
            if not update[key]:
                update[key] = value

        new_address = Address(**update)
        self.gm_service.validate_address(new_address)

        return self.get_customer_by_id(customer_id)

    @log
    def update_password(self, customer_id: int, new_password: str) -> Customer:
        customer = self.get_customer_by_id(customer_id)
        check_password_strength(new_password)
        password_hash = hash_password(new_password, customer.salt)
        update = {"customer_password_hash": password_hash}
        updated_customer = self.update_customer(customer_id, update)
        return updated_customer

    @log
    def order_history(self, customer_id: int) -> Optional[List[Order]]:
        history = self.order_dao.get_all_order_by_customer(customer_id)
        return history

    @log
    def make_order(self, customer_id: int) -> Order:
        return self.order_dao.create_order(customer_id)

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
