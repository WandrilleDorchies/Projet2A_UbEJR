import re
from typing import List, Optional

import phonenumbers as pn

from validate_email import validate_email
#from email_validator import validate_email

from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Address import Address
from src.Model.Customer import Customer
from src.Service.AddressService import AddressService
from src.Service.PasswordService import check_password_strength, create_salt, hash_password
from src.Service.UserService import UserService
from src.utils.log_decorator import log


class CustomerService:
    customer_dao: CustomerDAO
    address_service: AddressService
    user_service: UserService

    def __init__(
        self,
        customer_dao: CustomerDAO,
        address_service: AddressService,
        user_service: UserService,
    ):
        self.customer_dao = customer_dao
        self.address_service = address_service
        self.user_service = user_service
        self.pattern = r"^(?=.*[A-Za-zÀ-ÖØ-öø-ÿ])[-A-Za-zÀ-ÖØ-öø-ÿ ]+$"

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
        self.get_customer_by_id(customer_id)
        return self.address_service.get_address_by_customer_id(customer_id)

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
        # Check on first and last name
        if not re.match(self.pattern, first_name) or not re.match(self.pattern, last_name):
            raise ValueError(
                "[Customer Service] Cannot create customer: First name and last name "
                "must only contains letters"
            )
        # Check that phone number is valid
        try:
            phone_number = pn.parse(phone, "FR")
        except Exception:
            try:
                phone_number = pn.parse(phone)
            except Exception as e:
                raise ValueError(
                    "[CustomerService] Can't parse as FR number or foreign number"
                ) from e
        if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
            raise ValueError(f"[CustomerService] Cannot create: The number {phone} is invalid.")

        # normal  > E164 format : 06 12 12 12 12 > +33612121212
        valid_formatted_phone = pn.format_number(phone_number, pn.PhoneNumberFormat.E164)
        # Check that phone number is not already used
        existing_user = self.customer_dao.get_customer_by_phone(valid_formatted_phone)
        if existing_user is not None:
            raise ValueError(
                f"[CustomerService] Cannot create: customer with phone {valid_formatted_phone} "
                "already exists."
            )
        # Check that email is valid
        try:
            emailinfo = validate_email(mail, check_deliverability=True)
            validated_email = emailinfo.normalized
        except Exception as e:
            raise ValueError("[CustomerService] Cannot create: The email is invalid.") from e
        # check that email is not already used
        existing_user = self.customer_dao.get_customer_by_email(validated_email)
        if existing_user is not None:
            raise ValueError(
                f"[CustomerService] Cannot create: customer with email {validated_email} "
                "already exists."
            )
        check_password_strength(password)

        address = self.address_service.create_address(address_string)
        formatted_first_name = first_name.strip().capitalize()
        formatted_last_name = last_name.strip().upper()

        salt = create_salt()
        password_hash = hash_password(password, salt)

        customer = self.customer_dao.create_customer(
            formatted_first_name,
            formatted_last_name,
            valid_formatted_phone,
            validated_email,
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
                    "[Customer Service] Cannot update customer: First name "
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
            customer_mail = update["customer_mail"]
            try:
                emailinfo = validate_email(customer_mail, check_deliverability=True)
                update["customer_mail"] = emailinfo.normalized
            except Exception as e:
                raise ValueError("[CustomerService] Cannot update: The email is invalid.") from e

        updated_customer = self.customer_dao.update_customer(customer_id=customer_id, update=update)
        return updated_customer

    @log
    def update_address(self, customer_id: int, update: dict) -> Customer:
        customer = self.get_customer_by_id(customer_id)

        if all([value is None for value in update.values()]):
            raise ValueError("You must change at least one field.")

        address_id = customer.customer_address.address_id
        self.address_service.update_address(address_id, update)

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
