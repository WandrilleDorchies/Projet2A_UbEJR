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
    def get_all_orderables(self, in_menu=True) -> List[Union[Item, Bundle]]:
        orderables = self.orderable_dao.get_all_orderables()

        Orderables_in_menu = []
        for orderable in orderables:
            if orderable["orderable_type"] == "item":
                item = self.item_dao.get_item_by_orderable_id(orderable["orderable_id"])
                if (in_menu and item.check_availability()) or in_menu is False:
                    Orderables_in_menu.append(item)
            if orderable["orderable_type"] == "bundle":
                bundle = self.bundle_dao.get_bundle_by_orderable_id(orderable["orderable_id"])
                if (in_menu and bundle.check_availability()) or in_menu is False:
                    Orderables_in_menu.append(bundle)

        return Orderables_in_menu

    @log
    def get_orderable_from_menu(self, orderable_id: int) -> Union[Item, Bundle]:
        orderable = self.orderable_dao.get_orderable_by_id(orderable_id)
        if orderable is None:
            raise ValueError(
                f"[MenuService] Cannot get orderable: Orderable with ID {orderable_id} not found."
            )
        if orderable["orderable_type"] == "item":
            item = self.item_dao.get_item_by_orderable_id(orderable["orderable_id"])
            return item if item.check_availability() else None

        if orderable["orderable_type"] == "bundle":
            bundle = self.bundle_dao.get_bundle_by_orderable_id(orderable["orderable_id"])
            return bundle if bundle.check_availability() else None

    @log
    def remove_orderable_from_menu(self, orderable_id: int) -> Union[Item, Bundle]:
        orderable = self.orderable_dao.get_orderable_by_id(orderable_id)

        if orderable is None:
            raise ValueError(
                f"[MenuService] Cannot remove from menu: Orderable with ID {orderable_id} unknown."
            )

        if orderable["orderable_type"] == "item":
            orderable_instance = self.item_dao.get_item_by_orderable_id(orderable["orderable_id"])
        elif orderable["orderable_type"] == "bundle":
            orderable_instance = self.bundle_dao.get_bundle_by_orderable_id(
                orderable["orderable_id"]
            )

        if not orderable_instance.is_in_menu:
            raise ValueError(
                f"[MenuService] Cannot remove from menu: Orderable with ID {orderable_id} is "
                "already off the menu."
            )

        self.orderable_dao.update_orderable_state(orderable_id, False)
        orderable_instance.is_in_menu = False

        return orderable_instance

    @log
    def add_orderable_to_menu(self, orderable_id: int) -> Union[Item, Bundle]:
        orderable = self.orderable_dao.get_orderable_by_id(orderable_id)

        if orderable is None:
            raise ValueError(
                f"[MenuService] Cannot add to menu: Orderable with ID {orderable_id} unknown."
            )

        if orderable["orderable_type"] == "item":
            orderable_instance = self.item_dao.get_item_by_orderable_id(orderable["orderable_id"])
        elif orderable["orderable_type"] == "bundle":
            orderable_instance = self.bundle_dao.get_bundle_by_orderable_id(
                orderable["orderable_id"]
            )

        if orderable_instance.is_in_menu:
            raise ValueError(
                f"[MenuService] Cannot add to menu: Orderable with ID {orderable_id} is "
                "already on the menu."
            )

        if not orderable_instance.check_availability():
            if orderable["orderable_type"] == "item":
                raise ValueError(
                    f"[MenuService] Cannot add to menu: Item with ID {orderable_id} "
                    "is out of stock."
                )
            else:
                raise ValueError(
                    f"[MenuService] Cannot add to menu: Bundle with ID {orderable_id} "
                    "is not available (check dates or item stock)."
                )

        self.orderable_dao.update_orderable_state(orderable_id, True)
        orderable_instance.is_in_menu = True
        return orderable_instance

    @log
    def get_orderable_image(self, orderable_id: int) -> bytes:
        return self.orderable_dao.get_image_from_orderable(orderable_id)
