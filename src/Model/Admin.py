from pydantic import BaseModel


class Admin(BaseModel):
    """
    Represents an administrator in the system.

    Attributes
    ----------
        id_user (int): Unique identifier for the admin (references User).
    """
    id_user: int
