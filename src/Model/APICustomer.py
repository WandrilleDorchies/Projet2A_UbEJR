from pydantic import BaseModel

from .Address import Address


class APICustomer(BaseModel):
    """
    User representation in the API

    """

    id: int
    first_name: str
    last_name: str
    address: Address
