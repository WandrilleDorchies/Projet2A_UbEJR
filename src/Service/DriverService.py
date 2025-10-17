from src.DAO.DriverDAO import DriverDAO

from .UserService import UserService


class DriverService:
    def __init__(self, user_service: UserService, driver_dao: DriverDAO):
        self.driver_dao = driver_dao

    def accept_order(self, id_user: int, order: int) -> None:
        ## TODO

        return

    def delivery_start(self, id_user: int, order: int) -> None:
        ## TODO

        return

    def delivery_end(self, id_user: int, order: int) -> None:
        ## TODO

        return
