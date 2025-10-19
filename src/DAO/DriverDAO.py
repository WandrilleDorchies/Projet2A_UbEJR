from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class DriverDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def create_driver():
        pass

    def get_driver_by_id():
        pass

    def get_all_driver():
        pass

    def update_driver():
        pass

    def delete_driver():
        pass
