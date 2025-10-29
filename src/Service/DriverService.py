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
        driver = self.driver_dao.get_driver_by_phone(phone_number)
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot update driver: driver with phone {phone_number} not found."
            )
        return driver

    @log
    def get_all_driver(self) -> Optional[Driver]:
        drivers = self.driver_dao.get_all_drivers()
        return drivers

    @log
    def login(self, identifier: str, password: str) -> Optional[Driver]:
        return self.user_service.login(identifier, password)

    @log
    def create_driver(
        self, first_name: str, last_name: str, phone: str, password: str
    ) -> Optional[Driver]:
        check_password_strength(password)

        phone_number = pn.parse(phone, "FR")
        if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
            raise ValueError(f"The number {phone} is invalid.")

        salt = create_salt()
        password_hash = hash_password(password, salt)

        driver_phone = "0" + str(phone_number.national_number)
        created_driver = self.driver_dao.create_driver(
            first_name=first_name,
            last_name=last_name,
            phone=driver_phone,
            password_hash=password_hash,
            salt=salt,
        )
        return created_driver

    @log
    def update_driver(self, driver_id: int, update) -> Optional[Driver]:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot update driver: driver with ID {driver_id} not found."
            )
        updated_driver = self.driver_dao.update_driver(driver_id=driver_id, update=update)
        return updated_driver

    @log
    def accept_order(self, order_id: int, driver_id: int) -> Delivery:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot accept order: driver with ID {driver_id} not found."
            )

        if self.order_dao.get_order_by_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot accept order: order with ID {order_id} not found."
            )

        existing_delivery = self.delivery_dao.get_delivery_by_driver(driver_id)
        if existing_delivery:
            raise ValueError(f"[DriverService] Driver {driver_id} is already on a delivery.")

        delivery = self.delivery_dao.create_delivery(order_id, driver_id)
        return delivery

    @log
    def delivery_start(self, order_id: int, driver_id: int) -> Delivery:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot start delivery: driver with ID {driver_id} not found."
            )

        if self.delivery_dao.get_delivery_by_order_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot start delivery: order with ID {order_id} not found."
            )

        self.driver_dao.update_driver(driver_id, update={"driver_is_delivering": True})
        delivery = self.delivery_dao.update_delivery_state(order_id, 1)
        return delivery

    @log
    def delivery_end(self, order_id: int, driver_id: int) -> Delivery:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot end delivery: driver with ID {driver_id} not found."
            )

        if self.delivery_dao.get_delivery_by_order_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot end delivery: order with ID {order_id} not found."
            )

        self.driver_dao.update_driver(driver_id, update={"driver_is_delivering": False})
        delivery = self.delivery_dao.update_delivery_state(order_id, 2)
        return delivery

    @log
    def delete_driver(self, driver_id: int) -> None:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot delete: driver with ID {driver_id} not found."
            )

        self.driver_dao.delete_driver(driver_id)
