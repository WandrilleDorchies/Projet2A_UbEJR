from pydantic import BaseModel


class Delivery(BaseModel):
    """
    Represents a delivery assignment for an order.

    Attributes
    ----------
        id_order (int): Unique identifier of the order to be delivered.
        id_driver (int): Unique identifier of the driver assigned to the delivery.
        state (int, optional): Delivery status (0 = pending). Default is 0.
    """
    id_order: int
    id_driver: int
    state: int = 0
