from datetime import date, time
from typing import Dict, Union

from pydantic import BaseModel

from .Bundle import Bundle
from .Item import Item


class Order(BaseModel):
    """
    Represents a customer's order.

    Attributes
    ----------
        id_order (int): Unique identifier of the order.
        client_id (int): ID of the client.
        state (int, optional): Order status (0 = pending). Default is 0.
        items (Dict[Bundle | Item, int]): List of items and bundles in the order.
        date (date): Date of the order.
        time (time): Time of the order.
        is_paid (bool, optional): Whether the order has been paid. Default is False.
        is_prepared (bool, optional): Whether the order is prepared. Default is False.
    """

    order_id: int
    order_customer_id: int
    order_state: int = 0
    order_date: date
    order_time: time
    order_is_paid: bool = False
    order_is_prepared: bool = False
    order_items: Dict[Union[Bundle, Item], int]

    @property
    def order_price(self) -> float:
        """
        Calculate the price of the order (price of the item times its amount in the order)
        Return
        ------
        float:
            The total price of the order
        """
        total_price = 0.0
        for orderable, qty in self.order_items.items():
            total_price += orderable.price * qty

        return total_price
