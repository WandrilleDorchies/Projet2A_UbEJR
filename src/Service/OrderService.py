from typing import List, Optional

from src.DAO.OrderDAO import OrderDAO
from src.Model.Order import Order
from src.utils.log_decorator import log


class OrderService:
    order_dao: OrderDAO

    def __init__(self, order_dao: OrderDAO):
        self.order_dao = order_dao

    @log
    def get_order(self, order_id: int) -> Optional[Order]:
        order = self.order_dao.get_order_by_id(order_id)
        if order is None:
            raise ValueError(f"[Order Service] Cannot get: order with ID {order_id} not found.")
        return order

    @log
    def get_all_order(self) -> Optional[List[Order]]:
        orders = self.order_dao.get_all_order()
        return orders

    @log
    def get_all_order_by_customer(self, customer_id: int) -> Optional[List[Order]]:
        orders = self.order_dao.get_all_order_by_customer(customer_id)
        return orders

    @log
    def get_all_order_prepared(self) -> Optional[List[Order]]:
        orders = self.order_dao.get_all_order_prepared()
        return orders

    @log
    def create_order(self, customer_id) -> Order:
        new_order = self.order_dao.create_order(customer_id=customer_id)
        return new_order

    @log
    def update_order(self, order_id: int, update) -> Order:
        order = self.order_dao.get_order_by_id(order_id)
        if order is None:
            raise ValueError(f"[OrderService] Cannot update: order with ID {order_id} not found.")
        updated_order = self.order_dao.update_order(order_id=order_id, update=update)
        return updated_order

    @log
    def delete_order(self, order_id: int) -> None:
        order = self.order_dao.get_order_by_id(order_id)
        if order is None:
            raise ValueError(f"[OrderService] Cannot delete: order with ID {order_id} not found.")

        self.order_dao.delete_order_by_id(order_id)

    @log
    def calculate_price(self, order_id: int) -> float:
        """
        Calculates the total price of an order and updates the Order object.
        Currently applies only bundle reductions.
        Parameters
        ----------
        order_id : int
            The unique identifier of the order for which the total price
            will be calculated.

        Returns
        -------
        float:
            The total price of the order
        """
        order = self.order_dao.get_order_by_id(order_id)

        if order is None:
            raise ValueError(f"No order found with id {order_id}")

        return order.order_price
