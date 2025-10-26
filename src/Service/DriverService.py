from typing import Optional

from src.DAO.DriverDAO import DriverDAO
from src.Model.Driver import Driver
from src.utils.log_decorator import log

from .UserService import UserService


class DriverService:
    driver_dao: DriverDAO
    # ? user_service : UserService

    def __init__(self, user_service: UserService, driver_dao: DriverDAO):
        self.driver_dao = driver_dao
        # ? self.user_service = user_service

    @log
    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        driver = self.driver_dao.get_driver_by_id(driver_id)
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
        update_message_parts = []
        for field, value in update.items():
            update_message_parts.append(f"{field}={value}")

        updated_driver = self.driver_dao.update_driver(driver_id=driver_id, update=update)
        return updated_driver

    @log
    def accept_order(self, id_user: int, order: int) -> None:
        ## TODO

        return

    @log
    def delivery_start(self, id_user: int, order: int) -> None:
        self.driver_dao.update_driver_delivery_status(id_user, True)

        # TODO
        return

    @log
    def delivery_end(self, id_user: int, order: int) -> None:
        self.driver_dao.update_driver_delivery_status(id_user, False)
        # TODO
        return

    @log
    def delete_driver(self, driver_id: int) -> None:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if driver is None:
            raise ValueError(
                f"[DriverService] Cannot delete: driver with ID {driver_id} not found."
            )

        self.driver_dao.delete_driver_by_id(driver_id)
