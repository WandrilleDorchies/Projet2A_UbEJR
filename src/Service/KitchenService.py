import asyncio
from random import randint
from typing import TYPE_CHECKING, List, Optional

from src.DAO.OrderDAO import OrderDAO
from src.Service.DriverService import DriverService
from src.utils.log_decorator import log

if TYPE_CHECKING:
    from src.Model.Order import Order


class KitchenService:
    order_dao: OrderDAO
    """
    Periodically counts orders and notifies drivers when there are >5
    orders prepared but not delivered
    """

    def __init__(self, order_dao: OrderDAO, driver_service: DriverService):
        self.order_dao = order_dao
        self.driver_service = driver_service

    @log
    async def check_ready_orders(self):
        while True:
            # ready_orders: List[Optional[Order]] = self.order_dao.get_avaliable_orders_for_drivers()
            ready_order_count = randint(5, 10)
            # if len(ready_orders) > 5:
            if ready_order_count > 5:
                # await self.driver_service.notify_all_drivers(
                #    f"{len(ready_orders)} ready orders waiting!"
                # )
                await self.driver_service.notify_all_drivers(
                    f"{ready_order_count} ready orders waiting!"
                )
            await asyncio.sleep(5 * 10)
