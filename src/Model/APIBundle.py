from typing import Dict

from pydantic import BaseModel

from .APIItem import APIItem


class APIBundle(BaseModel):
    bundle_id: int
    orderable_id: int
    bundle_name: str
    bundle_description: str
    bundle_items: Dict[APIItem, int]
