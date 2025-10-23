from dotenv import load_dotenv

from src.DAO.BundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderableDAO import OrderableDAO
from src.DAO.UserRepo import UserRepo
from src.Model.Orderable import Orderable
from src.Service.BundleService import BundleService
from src.Service.ItemService import ItemService
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService

load_dotenv()
db_connector = DBConnector()
# Users - admin, customer, driver
user_repo = UserRepo(db_connector)
# Items and Bundles
orderable_dao = OrderableDAO(db_connector)
item_dao = ItemDAO(db_connector, orderable_dao)
item_service = ItemService(item_dao)
# bundle_dao = BundleDAO(db_connector)
# bundle_service = BundleService(bundle_dao)
# Order and deliveries
jwt_service = JwtService()
user_service = UserService(user_repo)
