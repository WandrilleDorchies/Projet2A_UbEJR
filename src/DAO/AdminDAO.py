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
        return Admin(**raw_admin)
