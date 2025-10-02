from pydantic import BaseModel


class Address(BaseModel):
    """
    Represents a physical address.

    Attributes
    ----------
        number (int): Street number.
        street (str): Street name.
        city (str): City name.
        postal_code (int): Postal or ZIP code.
        country (str): Country name.
    """
    number: int
    street: str
    city: str
    postal_code: int
    country: str
