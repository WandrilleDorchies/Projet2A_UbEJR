from pydantic import BaseModel


class Driver(BaseModel):
    """
    Represents a driver in the system.

    Attributes
    ----------
        id_user (int): Unique identifier for the driver (references User).
        id_delivering (bool, optional): Indicates if the driver is currently delivering. Default is False.
        phone (str): Driver's phone number.
    """
    id_user: int
    phone: str
    is_delivering: bool = False
