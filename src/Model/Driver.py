from .User import User


class Driver(User):
    """
    Represents a driver in the system.

    Attributes
    ----------
        phone (str): Driver's phone number.
        is_delivering (bool, optional): Indicates if the driver is currently delivering.
                                        Default is False.
    """

    phone: str
    is_delivering: bool = False
