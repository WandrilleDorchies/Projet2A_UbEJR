from typing import Optional

from src.Model.Driver import Driver
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class DriverDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def create_driver(
        self, first_name: str, last_name: str, phone: str, password_hash: str, salt: str
    ) -> Driver:
        raw_created_driver = self.db_connector.sql_query(
            """
            INSERT INTO Drivers (driver_id, driver_first_name, driver_last_name,
                                driver_phone, driver_password_hash, driver_salt,
                                driver_is_delivering)
            VALUES (DEFAULT, %(first_name)s, %(last_name)s, %(phone)s,
                    %(password_hash)s, %(salt)s, FALSE)
            RETURNING *;
            """,
            {
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "password_hash": password_hash,
                "salt": salt,
            },
            "one",
        )
        return Driver(**raw_created_driver)

    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        raw_driver = self.db_connector.sql_query(
            "SELECT * FROM Drivers WHERE driver_id=%s", [driver_id], "one"
        )
        if raw_driver is None:
            return None
        return Driver(**raw_driver)

    def get_all_drivers(self) -> Optional[list[Driver]]:
        raw_drivers = self.db_connector.sql_query("SELECT * FROM Drivers", return_type="all")
        if raw_drivers is None:
            return None
        return [Driver(**raw_driver) for raw_driver in raw_drivers]

    def update_driver_delivery_status(self, driver_id: int, is_delivering: bool) -> Driver:
        raw_updated_driver = self.db_connector.sql_query(
            """
            UPDATE Drivers
            SET driver_is_delivering=%(is_delivering)s
            WHERE driver_id=%(driver_id)s
            RETURNING *;
            """,
            {"driver_id": driver_id, "is_delivering": is_delivering},
            "one",
        )
        return Driver(**raw_updated_driver)

    def delete_driver(self, driver_id: int) -> None:
        self.db_connector.sql_query("DELETE FROM Drivers WHERE driver_id=%s", [driver_id], "none")
