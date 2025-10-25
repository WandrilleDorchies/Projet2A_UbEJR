from pydantic import BaseModel


class Delivery(BaseModel):
    """
    Represents a delivery assignment for an order.

    Attributes
    ----------
        delivery_order_id (int): Unique identifier of the order to be delivered.
        delivery_driver_id (int): Unique identifier of the driver assigned to the delivery.
        delivery_state (int, optional): Delivery status (0 = pending). Default is 0.
    """

    delivery_order_id: int
    delivery_driver_id: int
    delivery_state: int = 0
