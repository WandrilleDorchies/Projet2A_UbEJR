from src.DAO.OrderDAO import OrderDAO
from src.Model.Order import Order


class OrderService:
    order_dao: OrderDAO

    def __init__(self, order_dao: OrderDAO):
        self.item_dao = order_dao

    def get_order(self, order_id: int) -> Order | None:
        print(f"[OrderService] Getting order with ID: {order_id}")
        order = self.order_dao.get_order_by_id(order_id)
        print(f"[OrderService] DAO returned: {order}")
        return order

    def get_all_order(self) -> list[Order] | None:
        print("[OrderService] Getting all orders")
        orders = self.order_dao.get_all_order()
        print(f"[OrderService] DAO returned: {orders}")
        return orders

    def get_all_order_by_customer(self, order_customer_id) -> list[Order] | None:
        print(f"[OrderService] Getting all orders for customer {order_customer_id}")
        orders = self.order_dao.get_all_order_by_customer()
        print(f"[OrderService] DAO returned: {orders}")
        return orders

    def get_all_order_prepared(self) -> list[Order] | None:
        print("[OrderService] Getting all preparated orders")
        orders = self.order_dao.get_all_order_prepared()
        print(f"[OrderService] DAO returned: {orders}")
        return orders

    def create_order(self, customer_id) -> None:
        print(f" [OrderService] Creating order: customer_id={customer_id}")
        new_order = self.order_dao.create_order(customer_id=customer_id)
        print(f"[OrderService] DAO returned after creation: {new_order}")
        return new_order

    def update_order(self, order_id: int, update) -> None:
        update_message_parts = []
        for field, value in update.items():
            update_message_parts.append(f"{field}={value}")

        print(f"[OrderService] Updating order: {', '.join(update_message_parts)}")

        updated_order = self.order_dao.update_order(order_id=order_id, update=update)
        print(f"[orderService] DAO returned after creation: {updated_order}")
        return updated_order

    def delete_order(self, order_id: int) -> None:
        print(f"[OrderService] Deleting order with ID: {order_id}")

        order = self.order_dao.get_order_by_id(order_id)
        if order is None:
            raise ValueError(f"[OrderService] Cannot delete: order with ID {order_id} not found.")

        self.order_dao.delete_order_by_id(order_id)
        print(f"[OrderService] Order with ID {order_id} has been deleted.")
        # TODO Rajouter les commandes avec orderable, je ne sais pas à quoi ça correspond (Néo)

    def calculate_price(self, order_id: int) -> Order:
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
        Order
        """
        order = self.order_dao.get_order_by_id(order_id)

        if order is None:
            raise ValueError(f"No order found with id {order_id}")

        total_price = 0.0

        for orderable, quantity in order.order_items.items():
            # ITEM
            if orderable.__class__.__name__ == "Item":
                total_price += orderable.item_price * quantity
            # 📦 BUNDLE
            elif orderable.__class__.__name__ == "Bundle":
                bundle_price = 0.0
                # Add the price of each Item inside the Bundle
                for item, qty_in_bundle in orderable.bundle_items.items():
                    bundle_price += item.item_price * qty_in_bundle
                # Apply bundle percentage discount if any
                if orderable.bundle_reduction > 0:
                    bundle_price = bundle_price * (1 - orderable.bundle_reduction / 100)

                total_price += bundle_price * quantity
        order.order_total_price = round(total_price, 2)
        return order
