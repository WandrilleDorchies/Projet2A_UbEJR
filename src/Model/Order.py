from pydantic import BaseModel
from typing import List
from datetime import date, time
from Item import Item


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
    id_order: int
    client_id: int
    state: int = 0
    items: List[Item]
    date: date
    time: time
    is_paid: bool = False
    is_prepared: bool = False
