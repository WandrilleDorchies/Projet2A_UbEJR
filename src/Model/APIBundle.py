from typing import Dict

from .APIItem import APIItem
from .Orderable import Orderable


class APIBundle(Orderable):
    bundle_id: int
    orderable_id: int
    bundle_name: str
    bundle_description: str
    bundle_items: Dict[APIItem, int]

    def __init__(self, **args):
        args["orderable_type"] = "bundle"
        super().__init__(**args)

    def __eq__(self, other) -> bool:
        if not isinstance(other, APIBundle):
            return False
        return self.orderable_id == other.orderable_id

    def __hash__(self) -> str:
        return hash(self.orderable_id)

    @property
    def price(self) -> float:
        """
        Calculate the price of the bundle according to the reduction

        Return
        ------
        float:
            Price of the bundle
        """
        total = sum(item.price * qty for item, qty in self.bundle_items.items())
        return total * (1 - self.bundle_reduction / 100)
