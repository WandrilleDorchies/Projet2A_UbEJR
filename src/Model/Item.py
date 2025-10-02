from pydantic import BaseModel


class Item(BaseModel):
    """
    Represents an item/product in the system.

    Attributes
    ----------
        id_item (int): Unique identifier for the item.
        name (str): Name of the item.
        price (float): Price of the item.
        type (str): Category or type of item.
        description (str): Description of the item.
        stock (int): Current stock quantity.
    """
    id_item: int
    name: str
    price: float
    kind: str
    description: str
    stock: int
