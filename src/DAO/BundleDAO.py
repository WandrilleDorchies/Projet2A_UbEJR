from datetime import datetime
from typing import Optional

from src.Model.Bundle import Bundle
from src.Model.Item import Item

from .DBConnector import DBConnector


class BundleDAO:
    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector


    def insert_bundle(
        self,
        bundle_id: int,
        bundle_reduction: int,
        bundle_availability_start_date: datetime,
        bundle_availability_end_date: datetime,
        bundle_items: list[Item],
    ):
        raw_created_bundle = self.db_connector.sql_query(
            """
        INSERT INTO Bundle (bundle_id, bundle_reduction,
                            bundle_availability_start_date,
                            bundle_availability_end_date, bundle_items)
        VALUES (DEFAULT, %(bundle_id)s, %(bundle_reduction)s,
        %(bundle_availability_start_date)s,
        %(bundle_availability_end_date)s, %(bundle_items)s)
        RETURNING *;
        """,
            {
                "bundle_id": bundle_id,
                "bundle_reduction": bundle_reduction,
                "bundle_availability_start_date": bundle_availability_start_date,
                "bundle_availability_end_date": bundle_availability_end_date,
                "bundle_items": bundle_items,
            },
            "one",
        )
        # pyrefly: ignore

        return Bundle(**raw_created_bundle)


    def get_bundle_by_id(self, bundle_id: int) -> Optional[Bundle]:
        """
        Retrieve the bundle associated with a given id.

        Args
        ----
        bundle_id (int):
            Unique identifier of the bundle whose id is requested.

        Returns
        -------
        Bundle or None
            An Bundle object containing the id information
            if found in the database, None otherwise.
        """

        raw_bundle = self.db_connector.sql_query(
            "SELECT * FROM Bundle WHERE bundle_id = %(bundle_id)s",
            {"bundle_id": bundle_id},
            "one",
        )
        if raw_bundle is None:
            return None
        # pyrefly: ignore
        return Bundle(**raw_bundle)

    def get_all_bundle(self) -> Optional[list[Bundle]]:
        raw_bundles = self.db_connector.sql_query("SELECT * FROM Bundle", "all")

        if raw_bundles is None:
            return None

        bundles = [Bundle(**raw_bundle) for raw_bundle in raw_bundles]

        return bundles


    def update_bundle(
        self,
        bundle_id: int,
        bundle_reduction: int,
        bundle_availability_start_date: datetime,
        bundle_availability_end_date: datetime,
        bundle_items: list[Item],
    ):
        raw_update_bundle = self.db_connector.sql_query(
            """
        UPDATE Bundle SET bundle_reduction = %(bundle_reduction)s,
        bundle_availability_start_date=%(bundle_availability_start_date)s,
        bundle_availability_end_date=%(bundle_availability_end_date)s,
        bundle_items=%(bundle_items)s
        WHERE bundle_id=%(bundle_id)s RETURNING *;
        """,
            {"key": 1},
            "one",
        )

        return Bundle(**raw_update_bundle)


    def delete_bundle(self, bundle_id: int):
        raw_delete_address = self.db_connector.sql_query(
            """ DELETE FROM Bundle WHERE bundle_id=%s """,
            "one",
        )

        return Bundle(**raw_delete_address)
