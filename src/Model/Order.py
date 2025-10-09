from datetime import date, time
from typing import List

from pydantic import BaseModel

from .Item import Item


class Order(BaseModel):
    """
    Represents a customer's order.

    Attributes
    ----------
        id_order (int): Unique identifier of the order.
        client_id (int): ID of the client.
        state (int, optional): Order status (0 = pending). Default is 0.
        items (List[Item]): List of items in the order.
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
    order_items: List[Item]
