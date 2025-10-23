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

    def create_order(self, order_id, customer_id, prices, items, date, time) -> None:
        print(f" Creating order: order_id={order_id}")
        new_order = Order(
            order_id=id,
            customer_id=customer_id,
            prices=prices,
            items=items,
            date=date,
            time=time,
        )
        print(f"New Order object created: {new_order}")
        # TODO

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
            raise ValueError(
                f"[OrderService] Cannot delete: order with ID {order_id} not found."
            )

        self.order_dao.delete_order_by_id(order_id)
        print(f"[OrderService] Order with ID {order_id} has been deleted.")
        # TODO Rajouter les commandes avec orderable, je ne sais pas à quoi ça correspond (Néo) 