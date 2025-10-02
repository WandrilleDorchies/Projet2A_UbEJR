from pydantic import BaseModel


class Item(BaseModel):
    """
    Represents an item/product in the system.

    Attributes
    ----------
        id_item (int): Unique identifier for the item.
        name (str): Name of the item.
        price (float): Price of the item (>= 0).
        item_type (str): Category or type of item.
        description (str): Description of the item.
        stock (int): Current stock quantity (>= 0).
    """

    id_item: int
    name: str
    price: float
    item_type: str
    description: str
    stock: int
