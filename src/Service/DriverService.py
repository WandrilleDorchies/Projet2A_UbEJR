import logging
import re
from typing import Optional

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DriverDAO import DriverDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Delivery import Delivery
from src.Model.Driver import Driver
from src.Model.Order import Order, OrderState
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
        self.pattern = r"^(?=.*[A-Za-zÀ-ÖØ-öø-ÿ])[-A-Za-zÀ-ÖØ-öø-ÿ ]+$"

    @log
    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot find driver: driver with ID {driver_id} not found."
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
        """
        Allows the driver to login by calling the mutual user_service.login method,
        which also handles errors

        Parameters
        ----------
        identifier : str
            a phone number
        password : str
            The driver's password

        Returns
        -------
        Optional[Driver]
            A Driver object in case of successful login
        """
        return self.user_service.login(identifier, password)

    @log
    def get_driver_current_order(self, driver_id: int) -> Optional[Order]:
        """
        Retrieves the Order the driver is supposed to be handling

        Parameters
        ----------
        driver_id : int
            ID of the driver

        Returns
        -------
        Optional[Order]
            An Order, if the driver is currently handling one through a delivery

        Raises
        ------
        ValueError
            raised if there is no in progress delivery assigned to this driver
            and therefore no order
        """
        delivery = self.delivery_dao.get_driver_current_delivery(driver_id)
        if delivery is None or delivery.delivery_state == 2:
            raise ValueError(
                "[DriverService] Cannot get delivery: There isn't any delivery "
                "assigned to this driver."
            )

        return self.order_dao.get_order_by_id(delivery.delivery_order_id)

    @log
    def create_driver(
        self, first_name: str, last_name: str, phone: str, password: str
    ) -> Optional[Driver]:
        #
        validated_phone = self.user_service.identifier_validator(phone)
        if validated_phone is None or validated_phone["type"] != "phone":
            logging.error("[DriverService] Cannot create: The phone {phone} is invalid.")
            raise ValueError("Please enter a valid phone number !")
        # Check that phone number is not already used
        existing_user = self.driver_dao.get_driver_by_phone(validated_phone["identifier"])
        if existing_user is not None:
            logging.error(
                "[DriverService] Cannot create: customer "
                f"with phone {validated_phone['identifier']} "
                "already exists."
            )
            raise ValueError("This phone number is already associated with an account !")
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
        valid_formatted_phone = validated_phone["identifier"]
        created_driver = self.driver_dao.create_driver(
            first_name=formatted_first_name,
            last_name=formatted_last_name,
            phone=valid_formatted_phone,
            password_hash=password_hash,
            salt=salt,
        )
        return created_driver

    @log
    def update_driver(self, driver_id: int, update: dict) -> Optional[Driver]:
        self.get_driver_by_id(driver_id)

        if all([value is None for value in update.values()]):
            raise ValueError("You must change at least one field.")

        update = {key: value for key, value in update.items() if update[key]}

        if update.get("driver_first_name"):
            if not re.match(self.pattern, update.get("driver_first_name")):
                raise ValueError(
                    "[driver Service] Cannot update driver: First name must only contains letters"
                )
            update["driver_first_name"] = update["driver_first_name"].strip().capitalize()

        if update.get("driver_last_name"):
            if not re.match(self.pattern, update.get("driver_last_name")):
                raise ValueError(
                    "[driver Service] Cannot update driver: Last name must only contains letters"
                )

            update["driver_last_name"] = update["driver_last_name"].strip().upper()

        if update.get("driver_phone"):
            customer_phone = update["driver_phone"]
            validated_phone = self.user_service.identifier_validator(customer_phone)
            if validated_phone is None or validated_phone["type"] != "phone":
                raise ValueError(f"The number {update['driver_phone']} is invalid.")

            update["driver_phone"] = validated_phone["identifier"]

        updated_driver = self.driver_dao.update_driver(driver_id=driver_id, update=update)
        return updated_driver

    @log
    def start_delivery(self, order_id: int, driver_id: int) -> Delivery:
        driver = self.get_driver_by_id(driver_id)
        order = self.order_dao.get_order_by_id(order_id)

        if order.order_state != OrderState.PREPARED:
            raise ValueError(
                "[DriverService] Cannot start delivery: "
                f"Order isn't prepared, current state: {order.order_state.name}"
            )

        if driver.driver_is_delivering:
            raise ValueError(
                f"[DriverService] Cannot start delivery: Driver {driver_id} "
                "already has an active delivery"
            )

        self.delivery_dao.create_delivery(order_id, driver_id)
        self.driver_dao.update_driver(driver_id, update={"driver_is_delivering": True})
        self.order_dao.update_order_state(order_id, OrderState.DELIVERING.value)
        delivery = self.delivery_dao.update_delivery_state(order_id, 1)
        return delivery

    @log
    def end_delivery(self, order_id: int, driver_id: int) -> Delivery:
        self.get_driver_by_id(driver_id)

        order = self.order_dao.get_order_by_id(order_id)

        if order.order_state != OrderState.DELIVERING:
            raise ValueError(
                "[DriverService] Cannot end delivery: Order must be delivering to complete, "
                f"current state: {order.order_state.name}"
            )

        self.driver_dao.update_driver(driver_id, update={"driver_is_delivering": False})
        self.order_dao.update_order_state(order_id, OrderState.DELIVERED.value)
        delivery = self.delivery_dao.update_delivery_state(order_id, 2)
        return delivery

    @log
    def delete_driver(self, driver_id: int) -> None:
        self.get_driver_by_id(driver_id)
        self.driver_dao.delete_driver(driver_id)
