from typing import Dict

from pydantic import BaseModel

from .APIItem import APIItem


class APIBundle(BaseModel):
    bundle_name: str
    bundle_description: str
    bundle_items: Dict[APIItem, int]


    def __hash__(self):
        return hash((self.bundle_name, self.bundle_description))

    def __eq__(self, other):
        return (
            isinstance(other, APIBundle) and
            self.bundle_name == other.bundle_name and
            self.bundle_description == other.bundle_description and
            self.bundle_items == other.bundle_items
        )

    def __repr__(self):
        return (
            f"bundle_name={self.bundle_name}, "
            f"bundle_description={self.bundle_description}, "
            f"bundle_items={self.bundle_items} "
        )
