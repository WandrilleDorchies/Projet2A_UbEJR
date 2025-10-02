from pydantic import BaseModel


class Item(BaseModel):
    """
    Represents an item.

    Attributes
    ----------
        id_item (int): Unique item identifier.
        name (str): Item name.
        price (float): Price of the item. always >= 0.
        type_item (str): Type of consumable, for example Food, Drink, etc
        description (str): Long form description
        stock (int): current stock of the item. always >= 0.
    """

    id_item: int
    name: str
    price: float
    type_item: str
    description: str
    stock: int
