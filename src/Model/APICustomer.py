from pydantic import BaseModel

from .Address import Address


class APICustomer(BaseModel):
    """
    Customer representation in the API

    """

    id: int
    first_name: str
    last_name: str
    address: Address
    customer_phone: str
    customer_mail: str
