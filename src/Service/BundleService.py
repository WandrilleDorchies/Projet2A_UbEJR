from src.Model.Bundle import Bundle
from src.DAO.BundleDAO import BundleDAO


class BundleService:
    bundle_dao: BundleDAO
    def __init__(self, bundle_dao:BundleDAO):
        self.bundle_dao=bundle_dao

    # READ
    def get_bundle(self, bundle_id: int) -> Bundle | None:
        pass

    def get_all_bundles():
        pass
