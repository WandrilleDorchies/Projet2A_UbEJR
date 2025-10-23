from src.DAO.DriverDAO import DriverDAO
from src.Model.Driver import Driver

from .UserService import UserService


class DriverService:
    def __init__(self, user_service: UserService, driver_dao: DriverDAO):
        self.driver_dao = driver_dao

    def create_driver(
        self, user_id: int, first_name: str, last_name: str, password_hash: str, is_delivering: bool
    ) -> None:
        print("[DriverService] Creating driver")

        new_driver = Driver(
            driver_id=user_id,
            driver_first_name=first_name,
            driver_last_name=last_name,
            driver_password_hash=password_hash,
            driver_is_delivering=is_delivering,
        )

        print(f"[ItemService] New Item object created: {new_driver}")

        created_driver = self.driver_dao.create_driver(
            driver_id=user_id,
            driver_first_name=first_name,
            driver_last_name=last_name,
            driver_password_hash=password_hash,
            driver_is_delivering=is_delivering,
        )
        print(f"[DriverService] DAO returned after creation: {created_driver}")
        return created_driver

    def accept_order(self, id_user: int, order: int) -> None:
        ## TODO

        return

    def delivery_start(self, id_user: int, order: int) -> None:
        self.driver_dao.update_driver_delivery_status(id_user, True)
        # TODO
        return

    def delivery_end(self, id_user: int, order: int) -> None:
        self.driver_dao.update_driver_delivery_status(id_user, False)
        # TODO
        return
