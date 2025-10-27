from typing import Optional

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DriverDAO import DriverDAO
from src.Model.Delivery import Delivery
from src.Model.Driver import Driver
from src.utils.log_decorator import log


class DriverService:
    driver_dao: DriverDAO
    delivery_dao: DeliveryDAO

    def __init__(self, delivery_dao: DeliveryDAO, driver_dao: DriverDAO):
        self.driver_dao = driver_dao
        self.delivery_dao = delivery_dao

    @log
    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot update driver: driver with ID {driver_id} not found."
            )
        return driver

    @log
    def get_all_driver(self) -> Optional[Driver]:
        drivers = self.driver_dao.get_all_drivers()
        return drivers

    @log
    def create_driver(
        self, user_id: int, first_name: str, last_name: str, password_hash: str, is_delivering: bool
    ) -> Optional[Driver]:
        created_driver = self.driver_dao.create_driver(
            driver_id=user_id,
            driver_first_name=first_name,
            driver_last_name=last_name,
            driver_password_hash=password_hash,
            driver_is_delivering=is_delivering,
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

        if self.delivery_dao.get_delivery_by_id(order_id) is None:
            raise ValueError(
                f"[DriverService] Cannot accept order: order with ID {order_id} not found."
            )

        delivery = self.delivery_dao.create_delivery(order_id, driver_id)
        return delivery

    @log
    def delivery_start(self, order_id: int, driver_id: int) -> Delivery:
        if self.driver_dao.get_driver_by_id(driver_id) is None:
            raise ValueError(
                f"[DriverService] Cannot start delivery: driver with ID {driver_id} not found."
            )

        if self.delivery_dao.get_delivery_by_id(order_id) is None:
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

        if self.delivery_dao.get_delivery_by_id(order_id) is None:
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

        self.driver_dao.delete_driver_by_id(driver_id)
