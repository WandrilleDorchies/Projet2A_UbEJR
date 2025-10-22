from datetime import datetime
from typing import Dict

from .Item import Item
from .Orderable import Orderable


class Bundle(Orderable):
    bundle_id: int
    orderable_id: int
    bundle_reduction: int
    bundle_availability_start_date: datetime
    bundle_availability_end_date: datetime
    bundle_items: Dict[Item, int]

    def __init__(self, **args):
        args["orderable_type"] = "bundle"
        super().__init__(**args)

    def get_price(self) -> float:
        """
        Calculate the price of the bundle according to the reduction

        Return
        ------
        float:
            Price of the bundle
        """
        total = sum(item.get_price() * qty for item, qty in self.bundle_items.items())
        return total * (1 - self.bundle_reduction / 100)

    def check_availability(self) -> bool:
        """
        Check that all the items are available and that the bundle is currently purchasable

        Return
        ------
        bool:
            True if all the conditions are met
        """
        now = datetime.now()
        is_in_period = (
            self.bundle_availability_start_date <= now <= self.bundle_availability_end_date
        )

        all_items_available = all(
            item.check_availability() and item.item_stock >= qty
            for item, qty in self.bundle_items.items()
        )

        return is_in_period and all_items_available
