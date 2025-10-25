from abc import ABC, abstractmethod

from pydantic import BaseModel


class Orderable(BaseModel, ABC):
    orderable_id: int
    orderable_type: str

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def check_availability(self) -> bool:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass
