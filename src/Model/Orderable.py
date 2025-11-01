from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel


class Orderable(BaseModel, ABC):
    orderable_id: int
    orderable_type: Literal["item", "bundle"]
    orderable_image: bytes
    is_in_menu: bool = False

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def check_availability(self) -> bool:
        pass

    @abstractmethod
    def check_stock(self, quantity) -> bool:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass
