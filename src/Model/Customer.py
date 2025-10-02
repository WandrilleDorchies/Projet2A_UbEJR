from Address import Address
from User import User


class Customer(User):
    """
    Represents a customer in the system.

    Attributes
    ----------
        id_user (int): Unique identifier for the customer (references User).
        address (Address): Customer's physical address.
        phone (str): Customer's phone number.
        mail (str): Customer's email address.
    """

    address: Address
    phone: str
    mail: str
