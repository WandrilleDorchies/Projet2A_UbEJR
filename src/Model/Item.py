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
    item_type: str
    item_description: str
    item_stock: int
    item_in_menu: bool = True

    def __init__(self, **args):
        args["orderable_type"] = "item"
        super().__init__(**args)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.item_id == other.item_id

    def __hash__(self):
        return hash(self.item_id)

    def check_availability(self) -> bool:
        """
        Check that stock are available and that item is in the menu

        Return
        ------
        bool:
            True if all the conditions are met
        """
        return self.item_stock > 0 and self.item_in_menu
