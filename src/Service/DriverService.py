from typing import Optional

from src.DAO.DriverDAO import DriverDAO
from src.Model.Driver import Driver


class DriverService:
    def __init__(self, driver_dao: DriverDAO):
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
