from typing import Literal

from .Orderable import Orderable


class Item(Orderable):
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
        stock (int): Current stock quantity (>= 0).
    """

    item_id: int
    orderable_id: int
    item_name: str
    item_price: float
    item_type: Literal["Starter", "Main course", "Dessert", "Side dish", "Drink"]
    item_description: str
    item_stock: int

    def __init__(self, **args):
        args["orderable_type"] = "item"
        super().__init__(**args)

    def __hash__(self) -> int:
        return hash(self.orderable_id)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.orderable_id == other.orderable_id

    def check_availability(self) -> bool:
        """
        Check that stock are available and that item is in the menu

        Return
        ------
        bool:
            True if all the conditions are met
        """
        return self.item_stock > 0 and self.is_in_menu

    def check_stock(self, quantity) -> bool:
        return self.check_availability() and self.item_stock - quantity >= 0

    @property
    def price(self) -> float:
        return self.item_price
