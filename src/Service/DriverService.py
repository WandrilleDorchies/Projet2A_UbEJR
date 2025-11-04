import re
from typing import Optional

import phonenumbers as pn

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DriverDAO import DriverDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Delivery import Delivery
from src.Model.Driver import Driver
from src.Service.UserService import UserService
from src.utils.log_decorator import log

from .PasswordService import check_password_strength, create_salt, hash_password


class DriverService:
    driver_dao: DriverDAO
    order_dao: OrderDAO
    delivery_dao: DeliveryDAO
    user_service: UserService

    def __init__(
        self,
        delivery_dao: DeliveryDAO,
        driver_dao: DriverDAO,
        order_dao: OrderDAO,
        user_service: UserService,
    ):
        self.driver_dao = driver_dao
        self.delivery_dao = delivery_dao
        self.user_service = user_service
        self.order_dao = order_dao
        self.pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ\- ]+$"

    @log
    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot update driver: driver with ID {driver_id} not found."
            )
        return driver

    @log
    def get_driver_by_phone(self, phone_number: str) -> Optional[Driver]:
        driver = self.driver_dao.get_driver_by_phone(phone_number.strip())
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot update driver: driver with phone {phone_number} not found."
            )
        return driver

    @log
    def get_all_drivers(self) -> Optional[Driver]:
        drivers = self.driver_dao.get_all_drivers()
        return drivers

    @log
    def login(self, identifier: str, password: str) -> Optional[Driver]:
        return self.user_service.login(identifier, password)

    @log
    def create_driver(
        self, first_name: str, last_name: str, phone: str, password: str
    ) -> Optional[Driver]:
        phone_number = pn.parse(phone, "FR")
        if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
            raise ValueError(f"The number {phone} is invalid.")

        if not re.match(self.pattern, first_name) or not re.match(self.pattern, last_name):
            raise ValueError(
                "[Driver Service] Cannot create driver: First name and last name "
                "must only contains letters"
            )

        check_password_strength(password)
        salt = create_salt()
        password_hash = hash_password(password, salt)

        formatted_first_name = first_name.strip().capitalize()
        formatted_last_name = last_name.strip().upper()

        driver_phone = "0" + str(phone_number.national_number)
        created_driver = self.driver_dao.create_driver(
            first_name=formatted_first_name,
            last_name=formatted_last_name,
            phone=driver_phone,
            password_hash=password_hash,
            salt=salt,
        )
        return created_driver

    @log
    def update_driver(self, driver_id: int, update: dict) -> Optional[Driver]:
        self.driver_dao.get_driver_by_id(driver_id)

        if all([value is None for value in update.values()]):
            raise ValueError("You must change at least one field.")

        update = {key: value for key, value in update.items() if update[key]}

        if update.get("driver_first_name"):
            if not re.match(self.pattern, update.get("driver_first_name")):
                raise ValueError(
                    "[driver Service] Cannot update driver: First namemust only contains letters"
                )
            update["driver_first_name"] = update["driver_first_name"].strip().capitalize()

        if update.get("driver_last_name"):
            if not re.match(self.pattern, update.get("driver_last_name")):
                raise ValueError(
                    "[driver Service] Cannot update driver: Last name must only contains letters"
                )

            update["driver_last_name"] = update["driver_last_name"].strip().upper()

        if update.get("driver_phone"):
            phone_number = pn.parse(update["driver_phone"], "FR")
            if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
                raise ValueError(f"The number {update['driver_phone']} is invalid.")

            driver_phone = "0" + str(phone_number.national_number)
            update["driver_phone"] = driver_phone

        updated_driver = self.driver_dao.update_driver(driver_id=driver_id, update=update)
        return updated_driver

    @log
    def accept_order(self, order_id: int, driver_id: int) -> Delivery:
        driver = self.get_driver_by_id(driver_id)

        if self.order_dao.get_order_by_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot accept order: order with ID {order_id} not found."
            )

        if driver.driver_is_delivering:
            raise ValueError(f"[DriverService] Driver {driver_id} is already on a delivery.")

        delivery = self.delivery_dao.create_delivery(order_id, driver_id)
        return delivery

    @log
    def start_delivery(self, order_id: int, driver_id: int) -> Delivery:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot start delivery: driver with ID {driver_id} not found."
            )

        if self.delivery_dao.get_delivery_by_order_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot start delivery: order with ID {order_id} not found."
            )

        self.driver_dao.update_driver(driver_id, update={"driver_is_delivering": True})
        self.order_dao.update_order(order_id, update={"order_state": 1})
        delivery = self.delivery_dao.update_delivery_state(order_id, 1)
        return delivery

    @log
    def end_delivery(self, order_id: int, driver_id: int) -> Delivery:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot end delivery: driver with ID {driver_id} not found."
            )

        if self.delivery_dao.get_delivery_by_order_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot end delivery: order with ID {order_id} not found."
            )

        self.driver_dao.update_driver(driver_id, update={"driver_is_delivering": False})
        self.order_dao.update_order(order_id, update={"order_state": 2})
        delivery = self.delivery_dao.update_delivery_state(order_id, 2)
        return delivery

    @log
    def delete_driver(self, driver_id: int) -> None:
        self.driver_dao.get_driver_by_id(driver_id)
        self.driver_dao.delete_driver(driver_id)
