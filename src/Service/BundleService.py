from datetime import datetime
from typing import Dict, List, Optional

from src.DAO.BundleDAO import BundleDAO
from src.Model.Bundle import Bundle
from src.Model.Item import Item
from src.utils.log_decorator import log


class BundleService:
    bundle_dao: BundleDAO

    def __init__(self, bundle_dao: BundleDAO):
        self.bundle_dao = bundle_dao

    @log
    def get_bundle_by_id(self, bundle_id: int) -> Optional[Bundle]:
        bundle = self.bundle_dao.get_bundle_by_id(bundle_id)
        if bundle is None:
            raise ValueError(f"[BundleService] Cannot get: bundle with ID {bundle_id} not found.")
        return bundle

    @log
    def get_bundle_by_orderable_id(self, orderable_id: int) -> Optional[Bundle]:
        bundle = self.bundle_dao.get_bundle_by_orderable_id(orderable_id)
        if bundle is None:
            raise ValueError(
                f"[BundleService] Cannot get: bundle with ID {orderable_id} not found."
            )
        return bundle

    @log
    def get_all_bundles(self) -> Optional[List[Bundle]]:
        bundles = self.bundle_dao.get_all_bundle()
        return bundles

    @log
    def create_bundle(
        self,
        bundle_name: str,
        bundle_reduction: int,
        bundle_description: str,
        bundle_availability_start_date: datetime,
        bundle_availability_end_date: datetime,
        bundle_items: Dict[Item, int],
        is_in_menu: bool = False,
    ) -> Optional[Bundle]:
        create_bundle = self.bundle_dao.create_bundle(
            bundle_name=bundle_name,
            bundle_reduction=bundle_reduction,
            bundle_description=bundle_description,
            bundle_availability_start_date=bundle_availability_start_date,
            bundle_availability_end_date=bundle_availability_end_date,
            bundle_items=bundle_items,
            is_in_menu=is_in_menu,
        )
        return create_bundle

    @log
    def update_bundle(self, bundle_id: int, update: dict) -> Optional[Bundle]:
        bundle = self.bundle_dao.update_bundle(bundle_id=bundle_id, update=update)
        if bundle is None:
            raise ValueError(
                f"[BundleService] Cannot update: bundle with ID {bundle_id} not found."
            )
        return bundle

    @log
    def delete_bundle(self, bundle_id: int) -> None:
        bundle = self.bundle_dao.get_bundle_by_id(bundle_id)
        if bundle is None:
            raise ValueError(
                f"[BundleService] Cannot delete: bundle with ID {bundle_id} not found."
            )

        self.bundle_dao.delete_bundle(bundle_id)
