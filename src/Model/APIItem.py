from pydantic import BaseModel


class APIItem(BaseModel):
    """
    Represents an item/product in the system.

    Attributes
    ----------
        item_name (str): Name of the item.
        item_price (float): Price of the item (>= 0).
        item_type (str): Category or type of item.
        item_description (str): Description of the item.
    """

    item_name: str
    item_price: float
    item_type: str
    item_description: str

    def __hash__(self):
        return hash((self.item_name, self.item_price, self.item_type, self.item_description))

    def __eq__(self, other):
        return (
            isinstance(other, APIItem) and
            self.item_name == other.item_name and
            self.item_price == other.item_price and
            self.item_type == other.item_type and
            self.item_description == other.item_description
        )

    def __repr__(self):
        return (
            f"item_name={self.item_name}, "
            f"item_price={self.item_price}, "
            f"item_type={self.item_type}, "
            f"item_description={self.item_description}"
        )
