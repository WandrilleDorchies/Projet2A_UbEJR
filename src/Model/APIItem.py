from .Orderable import Orderable


class APIItem(Orderable):
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

    def __init__(self, **args):
        args["orderable_type"] = "item"
        super().__init__(**args)

    def __hash__(self) -> str:
        return hash(self.orderable_id)

    def __eq__(self, other):
        if not isinstance(other, APIItem):
            return False
        return self.orderable_id == other.orderable_id

    @property
    def price(self) -> float:
        return self.item_price
