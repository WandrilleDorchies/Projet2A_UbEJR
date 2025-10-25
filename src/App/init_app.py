from dotenv import load_dotenv

from src.DAO.BundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderableDAO import OrderableDAO
from src.DAO.OrderDAO import OrderDAO
from src.Service.ItemService import ItemService
from src.Service.JWTService import JwtService

load_dotenv()
db_connector = DBConnector()

# Items and Bundles
orderable_dao = OrderableDAO(db_connector)
item_dao = ItemDAO(db_connector, orderable_dao)
bundle_dao = BundleDAO(db_connector, orderable_dao, item_dao)
order_dao = OrderDAO(db_connector, orderable_dao, item_dao, bundle_dao)
item_service = ItemService(item_dao, order_dao)
# bundle_service = BundleService(bundle_dao)
# Order and deliveries

jwt_service = JwtService()
