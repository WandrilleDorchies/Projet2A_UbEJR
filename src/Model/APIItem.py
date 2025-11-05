from pydantic import BaseModel


class APIItem(BaseModel):
    """
    Represents an item/product in the system.

    Attributes
    ----------
        id_item (int): Unique identifier for the item.
        product_id (int): Identifier of the item as an orderable
        name (str): Name of the item.
        price (float): Price of the item (>= 0).
        item_type (str): Category or type of item.
        description (str): Description of the item.
    """

    item_id: int
    orderable_id: int
    item_name: str
    item_price: float
    item_type: str
    item_description: str
