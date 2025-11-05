from typing import List, Optional

from src.DAO.BundleDAO import BundleDAO
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderableDAO import OrderableDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Order import Order, OrderState
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
        self.valid_transition = {
            OrderState.PENDING: [OrderState.PAID, OrderState.CANCELLED],
            OrderState.PAID: [OrderState.PREPARED, OrderState.CANCELLED],
            OrderState.PREPARED: [OrderState.DELIVERING, OrderState.CANCELLED],
            OrderState.DELIVERING: [OrderState.DELIVERED, OrderState.CANCELLED],
            OrderState.DELIVERED: [],
            OrderState.CANCELLED: [],
        }

    @log
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        order = self.order_dao.get_order_by_id(order_id)
        if order is None:
            raise ValueError(f"[Order Service] Cannot find: order with ID {order_id} not found.")
        return order

    @log
    def get_all_orders(self, limit: int) -> Optional[List[Order]]:
        return self.order_dao.get_all_orders(limit)

    @log
    def get_all_orders_by_customer(self, customer_id: int) -> Optional[List[Order]]:
        return self.order_dao.get_all_orders_by_customer(customer_id)

    @log
    def get_customer_current_order(self, customer_id: int) -> Optional[Order]:
        return self.order_dao.get_customer_current_order(customer_id)

    @log
    def get_orders_by_state(
        self,
        state: OrderState,
    ) -> List[Order]:
        return self.order_dao.get_orders_by_state(state.value)

    @log
    def get_available_orders_for_drivers(self) -> List[Order]:
        return self.order_dao.get_orders_by_state(OrderState.PREPARED.value, order_by="ASC")

    @log
    def get_actives_orders(self) -> List[Order]:
        return self.order_dao.get_actives_orders()

    @log
    def create_order(self, customer_id) -> Order:
        orders = self.get_all_orders_by_customer(customer_id)
        states = [order.order_state.value for order in orders]

        if any(state < OrderState.DELIVERED.value for state in states):
            return self.get_customer_current_order(customer_id)

        new_order = self.order_dao.create_order(customer_id=customer_id)
        return new_order

    @log
    def update_order_state(self, order_id: int, new_state: OrderState) -> Optional[Order]:
        order = self.order_dao.get_order_by_id(order_id)

        if new_state not in self.valid_transition[order.order_state]:
            raise ValueError(
                "[OrderService] Cannot change state: Cannot go from "
                f"{order.order_state} to {new_state}."
            )

        updated_order = self.order_dao.update_order_state(order_id, new_state.value)
        return updated_order

    @log
    def mark_as_paid(self, order_id: int) -> Order:
        return self.update_order_state(order_id, OrderState.PAID)

    @log
    def mark_as_prepared(self, order_id: int) -> Order:
        return self.update_order_state(order_id, OrderState.PREPARED)

    @log
    def delete_order(self, order_id: int) -> None:
        self.get_order_by_id(order_id)
        self.order_dao.delete_order(order_id)

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
        raw_orderable = self.orderable_dao.get_orderable_by_id(orderable_id)

        if raw_orderable is None:
            raise ValueError(f"[OrderService] Orderable with ID {orderable_id} not found.")

        if raw_orderable["orderable_type"] == "item":
            orderable = self.item_dao.get_item_by_orderable_id(orderable_id)
            if not orderable.check_stock(quantity):
                raise ValueError(
                    f"[OrderService] Not enough stock for {orderable.item_name}"
                    f" (available: {orderable.item_stock})."
                )
            update_data = {"item_stock": orderable.item_stock - quantity}
            self.item_dao.update_item(orderable.item_id, update_data)

        if raw_orderable["orderable_type"] == "bundle":
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
    def remove_orderable_from_order(
        self, orderable_id: int, order_id: int, quantity: int = 1
    ) -> Order:
        """
        Remove an orderable to a given order

        Parameters
        ----------
        orderable_id : int
            ID of the item to remove.
        order_id : int
            ID of the order
        quantity : int, optional
            Number of units to remove (default is 1).
        """
        raw_orderable = self.orderable_dao.get_orderable_by_id(orderable_id)
        if raw_orderable is None:
            raise ValueError(f"[OrderService] Orderable with ID {orderable_id} not found.")
        quantity_in_order = self.order_dao.get_quantity_of_orderables(order_id, orderable_id)
        if quantity_in_order < quantity:
            raise ValueError(
                f"[OrderService] Trying to remove {quantity} of orderable {orderable_id} when "
                f"there is only {quantity_in_order} of it in the order !"
            )
        if raw_orderable["orderable_type"] == "item":
            orderable = self.item_dao.get_item_by_orderable_id(orderable_id)

            update_data = {"item_stock": orderable.item_stock + quantity}
            self.item_dao.update_item(orderable.item_id, update_data)

        if raw_orderable["orderable_type"] == "bundle":
            orderable = self.bundle_dao.get_bundle_by_orderable_id(orderable_id)

            for item, nb in orderable.bundle_items.items():
                update_data = {"item_stock": item.item_stock + nb * quantity}
                self.item_dao.update_item(item.item_id, update_data)

        return self.order_dao.remove_orderable_from_order(
            order_id, orderable.orderable_id, quantity
        )
