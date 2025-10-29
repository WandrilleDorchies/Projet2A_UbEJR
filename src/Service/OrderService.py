from typing import List, Optional

from src.DAO.BundleDAO import BundleDAO
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderableDAO import OrderableDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Order import Order
from src.utils.log_decorator import log


class OrderService:
    order_dao: OrderDAO
    orderable_dao: OrderableDAO
    item_dao: ItemDAO
    bundle_dao: BundleDAO

    def __init__(
        self,
        order_dao: OrderDAO,
        orderable_dao: OrderableDAO,
        item_dao: ItemDAO,
        bundle_dao: BundleDAO,
    ):
        self.order_dao = order_dao
        self.orderable_dao = orderable_dao
        self.item_dao = item_dao
        self.bundle_dao = bundle_dao

    @log
    def get_order(self, order_id: int) -> Optional[Order]:
        order = self.order_dao.get_order_by_id(order_id)
        if order is None:
            raise ValueError(f"[Order Service] Cannot get: order with ID {order_id} not found.")
        return order

    @log
    def get_all_orders(self) -> Optional[List[Order]]:
        orders = self.order_dao.get_all_orders()
        return orders

    @log
    def get_all_orders_by_customer(self, customer_id: int) -> Optional[List[Order]]:
        orders = self.order_dao.get_all_orders_by_customer(customer_id)
        return orders

    @log
    def get_all_orders_prepared(self) -> Optional[List[Order]]:
        orders = self.order_dao.get_all_orders_prepared()
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

        self.order_dao.delete_order(order_id)

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

    @log
    def add_orderable_to_order(self, orderable_id: int, order_id: int, quantity: int = 1) -> Order:
        """
        Adds an orderable to a given order if enough stock is available.

        Parameters
        ----------
        item_id : int
            ID of the item to add.
        order_id : int
            ID of the order
        quantity : int, optional
            Number of units to add (default is 1).
        """
        orderable_type = self.orderable_dao.get_type_by_id(orderable_id)

        if orderable_type is None:
            raise ValueError(f"[OrderService] Orderable with ID {orderable_id} not found.")

        if orderable_type == "item":
            orderable = self.item_dao.get_item_by_orderable_id(orderable_id)
            if not orderable.check_stock(quantity):
                raise ValueError(
                    f"[OrderService] Not enough stock for {orderable.item_name}"
                    f" (available: {orderable.item_stock})."
                )
            update_data = {"item_stock": orderable.item_stock - quantity}
            self.item_dao.update_item(orderable.item_id, update_data)

        if orderable_type == "bundle":
            orderable = self.bundle_dao.get_bundle_by_orderable_id(orderable_id)
            if not orderable.check_stock(quantity):
                raise ValueError(
                    f"[OrderService] Not enough stock for {orderable.bundle_name}"
                    f" (available: {orderable.get_stock()})."
                )

            for item, nb in orderable.bundle_items.items():
                update_data = {"item_stock": item.item_stock - nb * quantity}
                self.item_dao.update_item(item.item_id, update_data)

        return self.order_dao.add_orderable_to_order(order_id, orderable.orderable_id, quantity)

    @log
    def remove_orderable_to_order(
        self, orderable_id: int, order_id: int, quantity: int = 1
    ) -> Order:
        """
        Remove an orderable to a given order

        Parameters
        ----------
        item_id : int
            ID of the item to remove.
        order_id : int
            ID of the order
        quantity : int, optional
            Number of units to remove (default is 1).
        """
        orderable_type = self.orderable_dao.get_type_by_id(orderable_id)
        if orderable_type is None:
            raise ValueError(f"[OrderService] Orderable with ID {orderable_id} not found.")

        if orderable_type == "item":
            orderable = self.item_dao.get_item_by_orderable_id(orderable_id)

            update_data = {"item_stock": orderable.item_stock + quantity}
            self.item_dao.update_item(orderable.item_id, update_data)

        if orderable_type == "bundle":
            orderable = self.bundle_dao.get_bundle_by_orderable_id(orderable_id)

            for item, nb in orderable.bundle_items.items():
                update_data = {"item_stock": item.item_stock + nb * quantity}
                self.item_dao.update_item(item.item_id, update_data)

        return self.order_dao.remove_orderable_from_order(
            order_id, orderable.orderable_id, quantity
        )
