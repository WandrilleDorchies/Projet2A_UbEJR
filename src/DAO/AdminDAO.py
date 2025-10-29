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
        raw_admin = self.db_connector.sql_query("SELECT * from Admin", return_type="one")
        raw_admin_mapped = self._map_db_to_model(raw_admin)
        return Admin(**raw_admin_mapped)

    @staticmethod
    def _map_db_to_model(raw_admin: dict) -> dict:
        """
        Map the column name of the table into the correct name of the arguments
        to build an Admin instance (beacause it inherits from User)
        """
        return {
            "id": raw_admin["admin_id"],
            "first_name": raw_admin["admin_first_name"],
            "last_name": raw_admin["admin_last_name"],
            "password": raw_admin["admin_password_hash"],
            "salt": raw_admin["admin_salt"],
            "created_at": raw_admin["admin_created_at"],
        }
