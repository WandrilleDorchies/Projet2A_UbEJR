from datetime import datetime

from src.Model.Admin import Admin
from src.utils.log_decorator import log
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class AdminDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    # READ
    @log
    def get_admin(self) -> Admin:
        raw_admin = self.db_connector.sql_query("SELECT * from Admins", return_type="one")
        if raw_admin is None:
            return None

        raw_admin_mapped = self._map_db_to_model(raw_admin)
        return Admin(**raw_admin_mapped)

    # CREATE
    @log
    def create_admin(
        self, username: str, first_name: str, last_name: str, password: str, salt: str
    ) -> Admin:
        if self.get_admin() is not None:
            raise ValueError("It can only exists one admin.")
        raw_admin = self.db_connector.sql_query(
            """INSERT INTO Admins (username, admin_first_name, admin_last_name, admin_created_at,
                                   admin_password_hash, admin_salt)
               VALUES (%(username)s, %(admin_first_name)s, %(admin_last_name)s,
                       %(admin_created_at)s, %(admin_password_hash)s, %(admin_salt)s)
               RETURNING *;""",
            {
                "username": username,
                "admin_first_name": first_name,
                "admin_last_name": last_name,
                "admin_created_at": datetime.now(),
                "admin_password_hash": password,
                "admin_salt": salt,
            },
            "one",
        )
        return raw_admin

    # UPDATE
    @log
    def update_admin_password(self, new_password) -> Admin:
        self.db_connector.sql_query(
            """
            UPDATE Admins
            SET admin_password_hash = %s;
            """,
            [new_password],
            "none",
        )
        return self.get_admin()

    @staticmethod
    def _map_db_to_model(raw_admin: dict) -> dict:
        """
        Map the column name of the table into the correct name of the arguments
        to build an Admin instance (beacause it inherits from User)
        """
        return {
            "id": raw_admin["admin_id"],
            "username": raw_admin["username"],
            "first_name": raw_admin["admin_first_name"],
            "last_name": raw_admin["admin_last_name"],
            "password": raw_admin["admin_password_hash"],
            "salt": raw_admin["admin_salt"],
            "created_at": raw_admin["admin_created_at"],
        }
