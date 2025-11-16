import logging
from typing import Literal, Union

import phonenumbers as pn
from email_validator import EmailNotValidError, validate_email

from src.DAO.AdminDAO import AdminDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DriverDAO import DriverDAO
from src.Model.Admin import Admin
from src.Model.Customer import Customer
from src.Model.Driver import Driver
from src.Service.PasswordService import (
    check_password_strength,
    hash_password,
    validate_password,
)
from src.utils.log_decorator import log


class UserService:
    def __init__(self, customer_dao: CustomerDAO, driver_dao: DriverDAO, admin_dao: AdminDAO):
        self.customer_dao = customer_dao
        self.driver_dao = driver_dao
        self.admin_dao = admin_dao

    @log
    def login(
        self, identifier: str, password: str, user_type: Literal["customer", "driver", "admin"]
    ) -> Union[Customer, Driver, Admin]:
        user = None
        validated_identifier = self.identifier_validator(identifier)
        if user_type == "customer" and validated_identifier["type"] == "phone":
            user = self.customer_dao.get_customer_by_phone(validated_identifier["identifier"])
        elif user_type == "customer" and validated_identifier["type"] == "email":
            user = self.customer_dao.get_customer_by_email(validated_identifier["identifier"])
        elif user_type == "driver" and validated_identifier["type"] == "phone":
            user = self.driver_dao.get_driver_by_phone(validated_identifier["identifier"])
        elif user_type == "admin" and identifier == "adminsee":
            user = self.admin_dao.get_admin()
        if not user:
            logging.error(f"[UserService] Login failed for user with identifier: {identifier}")
            raise ValueError(f"[UserService] User not found with identifier: {identifier}")

        validate_password(user, password)

        return user

    @log
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
        user_type: Literal["customer", "driver", "admin"],
    ) -> Union[Customer, Driver, Admin]:
        user = self._get_user_by_type(user_id, user_type)

        validate_password(user, old_password)

        check_password_strength(new_password)

        new_hashed = hash_password(new_password, user.salt)

        if user_type == "customer":
            return self.customer_dao.update_customer(
                user_id, {"customer_password_hash": new_hashed}
            )
        elif user_type == "driver":
            return self.driver_dao.update_driver(user_id, {"driver_password_hash": new_hashed})
        elif user_type == "admin":
            return self.admin_dao.update_admin_password(new_hashed)

    def _get_user_by_type(self, user_id: int, user_type: Literal["customer", "driver", "admin"]):
        if user_type == "customer":
            return self.customer_dao.get_customer_by_id(user_id)
        elif user_type == "driver":
            return self.driver_dao.get_driver_by_id(user_id)
        elif user_type == "admin":
            return self.admin_dao.get_admin()

    @log
    def identifier_validator(self, identifier: str) -> dict:
        logging.info("[UserService] Parsing identifier as email...")
        try:
            emailinfo = validate_email(identifier, check_deliverability=True)
            return {"type": "email", "identifier": emailinfo.normalized}
        except EmailNotValidError:
            pass
        logging.info("[UserService] Parsing identifier as french phone...")
        try:
            phone_number = pn.parse(identifier, "FR")
            if pn.is_valid_number(phone_number) and pn.is_possible_number(phone_number):
                return {
                    "type": "phone",
                    "identifier": pn.format_number(phone_number, pn.PhoneNumberFormat.E164),
                }
        except pn.NumberParseException:
            pass
        logging.info("[UserService] Parsing identifier as international phone...")
        try:
            phone_number = pn.parse(identifier)
            if pn.is_valid_number(phone_number) and pn.is_possible_number(phone_number):
                return {
                    "type": "phone",
                    "identifier": pn.format_number(phone_number, pn.PhoneNumberFormat.E164),
                }
        except pn.NumberParseException:
            pass
        logging.warning("Identifier could not be parsed. Register/Login will fail.")
        return {"type": None, "identifier": None}
