from src.DAO.OrderDAO import OrderDAO
from src.Model.Order import Order


class OrderService:
    order_dao: OrderDAO

    def __init__(self, order_dao: OrderDAO):
        self.item_dao = order_dao

    def add_order(self, order_id, customer_id, prices, items, date, time) -> None:
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
        # TO DO
