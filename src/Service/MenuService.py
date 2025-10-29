from typing import List, Union

from src.DAO.BundleDAO import BundleDAO
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderableDAO import OrderableDAO
from src.Model.Bundle import Bundle
from src.Model.Item import Item
from src.utils.log_decorator import log


class MenuService:
    orderable_dao: OrderableDAO
    item_dao: ItemDAO
    bundle_dao: BundleDAO

    def __init__(self, orderable_dao: OrderableDAO, item_dao: ItemDAO, bundle_dao: BundleDAO):
        self.orderable_dao = orderable_dao
        self.item_dao = item_dao
        self.bundle_dao = bundle_dao

    @log
    def get_all_orderable_in_menu(self) -> List[Union[Item, Bundle]]:
        orderables = self.orderable_dao.get_all_orderable_in_menu()

        Orderables_in_menu = []
        for orderable in orderables:
            if orderable["orderable_type"] == "item":
                item = self.item_dao.get_item_by_orderable_id(orderable["orderable_id"])
                Orderables_in_menu.append(item)
            if orderable["orderable_type"] == "bundle":
                bundle = self.bundle_dao.get_bundle_by_orderable_id(orderable["orderable_id"])
                Orderables_in_menu.append(bundle)

        return Orderables_in_menu

    @log
    def remove_orderable_from_menu(self, orderable_id: int) -> Union[Item, Bundle]:
        orderable = self.orderable_dao.get_orderable_by_id(orderable_id)

        if orderable is None:
            raise ValueError(
                f"[MenuService] Cannot remove to menu: Orderable with ID {orderable_id} unknown "
            )
        if orderable["is_in_menu"] is False:
            raise ValueError(
                f"[MenuService] Cannot add to menu: Orderable with ID {orderable_id} is "
                "already off the menu."
            )

        orderable = self.orderable_dao.update_orderable_state(orderable_id, False)

        if orderable["orderable_type"] == "item":
            return self.item_dao.get_item_by_orderable_id(orderable.orderable_id)

        if orderable["orderable_type"] == "bundle":
            return self.bundle_dao.get_bundle_by_orderable_id(orderable.orderable_id)

    @log
    def add_orderable_to_menu(self, orderable_id: int) -> Union[Item, Bundle]:
        orderable = self.orderable_dao.get_orderable_by_id(orderable_id)

        if orderable is None:
            raise ValueError(
                f"[MenuService] Cannot add to menu: Orderable with ID {orderable_id} unknown "
            )
        if orderable["is_in_menu"] is True:
            raise ValueError(
                f"[MenuService] Cannot add to menu: Orderable with ID {orderable_id} is "
                "already on the menu."
            )

        orderable = self.orderable_dao.update_orderable_state(orderable_id, True)

        if orderable["orderable_type"] == "item":
            return self.item_dao.get_item_by_orderable_id(orderable.orderable_id)

        if orderable["orderable_type"] == "bundle":
            return self.bundle_dao.get_bundle_by_orderable_id(orderable.orderable_id)
