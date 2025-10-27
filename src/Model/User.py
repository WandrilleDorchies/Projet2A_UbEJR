from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a basic user in the sytem.

    Attributes
    ----------
    id (int): id of the user
    first_name (str): first name
    last_name (str): last name
    created_at (datetime): date of the creation of the user
    password (str): password
    salt (str): the salt, unique for each user
    """

    id: int
    first_name: str
    last_name: str
    """
    created_at: datetime
    """
    password_hash: str
    salt: str
    role: Literal["admin", "driver", "customer"]
    """
    # for everyone
    email: str
    # for customer and driver
    phone: Optional[str]
    # customer specific
    address_id: Optional[int]
    # driver specific
    is_delivering: bool
    """
