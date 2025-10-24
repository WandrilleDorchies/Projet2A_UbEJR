from src.utils.log_decorator import log
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class OrderableDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    # CREATE
    @log
    def create_orderable(self, orderable_type: str) -> int:
        """
        Create an orderable

        Return
        ------
        int:
            The orderable_id of the created instance
        """
        result = self.db_connector.sql_query(
            """
            INSERT INTO Orderables (orderable_type)
            VALUES (%(orderable_type)s)
            RETURNING orderable_id;
            """,
            {"orderable_type": orderable_type},
            "one",
        )
        return result["orderable_id"]
