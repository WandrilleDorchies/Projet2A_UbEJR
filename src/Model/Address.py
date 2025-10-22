from pydantic import BaseModel


class Address(BaseModel):
    """
    Represents a physical address.

    Attributes
    ----------
        address_id (int): Unique identifier
        address_number (int): Street number.
        address_street (str): Street name.
        address_city (str): City name.
        address_postal_code (int): Postal or ZIP code.
        address_country (str): Country name.
    """

    address_id: int
    address_number: int
    address_street: str
    address_city: str
    address_postal_code: int
    address_country: str
