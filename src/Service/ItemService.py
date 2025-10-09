from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import Item


class ItemService:
    item_dao: ItemDAO

    def __init__(self, item_dao: ItemDAO):
        self.item_dao = item_dao

    def get_item(self, item_id: int) -> Item | None:
        print(f"[ItemService] Getting item with ID: {item_id}")
        item = self.item_dao.get_item_by_id(item_id)
        print(f"[ItemService] DAO returned: {item}")
        return item


        
