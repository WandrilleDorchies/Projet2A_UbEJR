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

    address_number: int
    address_street: str
    address_city: str
    address_postal_code: int
    address_country: str
