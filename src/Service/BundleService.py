from src.Model.Bundle import Bundle


class BundleService:
    def __init__(self, bundle_dao):
        pass

    def compute_bundle_price(self, bundle: Bundle) -> float:
        return sum([Item.item_price for Item in bundle.bundle_items]) * (
            1 - (bundle.bundle_reduction / 100)
        )
