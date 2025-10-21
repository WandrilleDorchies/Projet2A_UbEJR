from datetime import datetime
from typing import Dict

from pydantic import BaseModel

from .Item import Item


class Bundle(BaseModel):
    bundle_id: int
    bundle_reduction: int
    bundle_availability_start_date: datetime
    bundle_availability_end_date: datetime
    bundle_items: Dict[Item, int]
