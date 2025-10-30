from typing import Dict, List, Optional

from src.utils.log_decorator import log
from src.utils.singleton import Singleton

from .DBConnector import DBConnector


class OrderableDAO(metaclass=Singleton):
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    # CREATE
    @log
    def create_orderable(self, orderable_type: str, is_in_menu: bool = False) -> int:
        """
        Create an orderable

        Return
        ------
        int:
            The orderable_id of the created instance
        """
        result = self.db_connector.sql_query(
            """
            INSERT INTO Orderables (orderable_type, is_in_menu)
            VALUES (%(orderable_type)s, %(is_in_menu)s)
            RETURNING orderable_id;
            """,
            {"orderable_type": orderable_type, "is_in_menu": is_in_menu},
            "one",
        )
        return result["orderable_id"]

    @log
    def get_orderable_by_id(self, orderable_id: int) -> Optional[Dict]:
        raw_orderable = self.db_connector.sql_query(
            "SELECT * FROM Orderables WHERE orderable_id=%s;", [orderable_id], "one"
        )
        return raw_orderable if raw_orderable else None

    @log
    def get_all_orderables(self) -> List[Dict]:
        raw_orderables = self.db_connector.sql_query("SELECT * FROM Orderables", return_type="all")
        if not raw_orderables:
            return []

        return raw_orderables

    @log
    def get_all_orderable_in_menu(self) -> List[Dict]:
        raw_orderables = self.db_connector.sql_query(
            "SELECT * FROM Orderables WHERE is_in_menu=true;", return_type="all"
        )
        if not raw_orderables:
            return []

        return raw_orderables

    @log
    def update_orderable_state(self, orderable_id: int, is_in_menu: bool) -> Dict:
        raw_orderable = self.db_connector.sql_query(
            """UPDATE Orderables
            SET is_in_menu = %(is_in_menu)s
            WHERE orderable_id = %(orderable_id)s
            RETURNING *;""",
            {"is_in_menu": is_in_menu, "orderable_id": orderable_id},
            "one",
        )
        return raw_orderable

    def _is_in_menu(self, orderable_id: int) -> bool:
        raw_orderable = self.db_connector.sql_query(
            "SELECT is_in_menu FROM Orderables WHERE orderable_id=%s;", [orderable_id], "one"
        )
        return raw_orderable["is_in_menu"] if raw_orderable else None
