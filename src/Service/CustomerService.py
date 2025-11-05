import re
from typing import List, Optional

import phonenumbers as pn
from validate_email import validate_email

from src.DAO.AddressDAO import AddressDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Address import Address
from src.Model.Customer import Customer
from src.Service.GoogleMapService import GoogleMapService
from src.Service.PasswordService import check_password_strength, create_salt, hash_password
from src.Service.UserService import UserService
from src.utils.log_decorator import log


class CustomerService:
    customer_dao: CustomerDAO
    address_dao: AddressDAO
    gm_service: GoogleMapService
    user_service: UserService

    def __init__(
        self,
        customer_dao: CustomerDAO,
        address_dao: AddressDAO,
        gm_service: GoogleMapService,
        user_service: UserService,
    ):
        self.customer_dao = customer_dao
        self.address_dao = address_dao
        self.gm_service = gm_service
        self.user_service = user_service
        self.pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ\- ]+$"

    @log
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError(
                f"[CustomerService] Cannot find: customer with ID {customer_id} not found."
            )
        return customer

    @log
    def get_address_by_customer_id(self, customer_id: int) -> Address:
        return self.address_dao.get_address_by_customer_id(customer_id)

    @log
    def get_customer_by_email(self, customer_email: str) -> Optional[Customer]:
        return self.customer_dao.get_customer_by_email(customer_email)

    @log
    def get_customer_by_phone(self, customer_phone: int) -> Optional[Customer]:
        return self.customer_dao.get_customer_by_phone(customer_phone)

    @log
    def get_all_customers(self) -> Optional[List[Customer]]:
        customers = self.customer_dao.get_all_customers()
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
        formatted_mail = mail.lower().strip()
        existing_user = self.customer_dao.get_customer_by_email(formatted_mail)
        if existing_user is not None:
            raise ValueError(
                f"[CustomerService] Cannot create: customer with email {formatted_mail} "
                "already exists."
            )

        formatted_phone = phone.strip()
        existing_user = self.customer_dao.get_customer_by_phone(formatted_phone)
        if existing_user is not None:
            raise ValueError(
                f"[CustomerService] Cannot create: customer with phone {formatted_phone} "
                "already exists."
            )
        if not re.match(self.pattern, first_name) or not re.match(self.pattern, last_name):
            raise ValueError(
                "[Customer Service] Cannot create customer: First name and last name "
                "must only contains letters"
            )

        phone_number = pn.parse(formatted_phone, "FR")
        if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
            raise ValueError(f"[CustomerService] Cannot create: The number {phone} is invalid.")

        is_valid_email = validate_email(
            formatted_mail, check_blacklist=False, check_dns=False, check_smtp=False
        )

        if not is_valid_email:
            raise ValueError("[CustomerService] Cannot create: The email is not valid.")

        address = self.gm_service.validate_address(address_string)
        if address is None:
            raise ValueError(
                "[CustomerService] Cannot create: customer address "
                "is invalid or outside the delivery zone."
            )

        check_password_strength(password)

        formatted_first_name = first_name.strip().capitalize()
        formatted_last_name = last_name.strip().upper()

        customer_phone = "0" + str(phone_number.national_number)

        salt = create_salt()
        password_hash = hash_password(password, salt)

        customer = self.customer_dao.create_customer(
            formatted_first_name,
            formatted_last_name,
            customer_phone,
            formatted_mail,
            password_hash,
            salt,
            address.address_id,
        )

        return customer

    @log
    def login_customer(self, identifier: str, password: str) -> Optional[Customer]:
        return self.user_service.login(identifier, password, "customer")

    @log
    def update_customer(self, customer_id: int, update: dict) -> Customer:
        self.get_customer_by_id(customer_id)

        if all([value is None for value in update.values()]):
            raise ValueError("You must change at least one field.")

        update = {key: value for key, value in update.items() if update[key]}

        if update.get("customer_first_name"):
            if not re.match(self.pattern, update.get("customer_first_name")):
                raise ValueError(
                    "[Customer Service] Cannot update customer: First name"
                    "must only contains letters"
                )
            update["customer_first_name"] = update["customer_first_name"].strip().capitalize()

        if update.get("customer_last_name"):
            if not re.match(self.pattern, update.get("customer_last_name")):
                raise ValueError(
                    "[Customer Service] Cannot update customer: Last name "
                    "must only contains letters"
                )

            update["customer_last_name"] = update["customer_last_name"].strip().upper()

        if update.get("customer_phone"):
            phone_number = pn.parse(update["customer_phone"], "FR")
            if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
                raise ValueError(f"The number {update['customer_phone']} is invalid.")

            update["customer_phone"] = "0" + str(phone_number.national_number)

        if update.get("customer_mail"):
            is_valid_email = validate_email(
                update["customer_mail"],
                check_blacklist=False,
                check_dns=False,
                check_smtp=False,
            )

            if not is_valid_email:
                raise ValueError("[CustomerService] Cannot create: The email is not valid.")

        updated_customer = self.customer_dao.update_customer(customer_id=customer_id, update=update)
        return updated_customer

    @log
    def update_address(self, customer_id: int, update: dict) -> Customer:
        customer = self.get_customer_by_id(customer_id)

        if all([value is None for value in update.values()]):
            raise ValueError("You must change at least one field.")

        update = {key: value for key, value in update.items() if update[key]}

        update["address_id"] = customer.address_id
        new_address = Address(**update)
        self.gm_service.validate_address(new_address)

        return self.get_customer_by_id(customer_id)

    @log
    def update_password(self, customer_id: int, old_password: str, new_password: str) -> Customer:
        self.get_customer_by_id(customer_id)
        return self.user_service.change_password(
            customer_id, old_password, new_password, "customer"
        )

    # @log
    # def update_phone(self, customer_id: int, phone: str) -> Customer:

    #     phone_number = pn.parse(phone, "FR")
    #     if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
    #         raise ValueError(f"The number {phone} is invalid.")

    #     customer_phone = "0" + str(phone_number.national_number)

    #     update = {"customer_phone": customer_phone}
    #     updated_customer = self.update_customer(customer_id, update)
    #     return updated_customer

    @log
    def delete_customer(self, customer_id: int) -> None:
        """
        Deletes a customer from the database by its ID.

        Parameters
        ----------
        customer_id : int
            The ID of the customer to delete.
        """
        self.get_customer_by_id(customer_id)
        self.customer_dao.delete_customer(customer_id)
