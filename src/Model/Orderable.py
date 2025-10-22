from abc import ABC, abstractmethod

from pydantic import BaseModel


class Orderable(BaseModel, ABC):
    orderable_id: int
    orderable_type: str

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def check_availability(self) -> bool:
        pass
