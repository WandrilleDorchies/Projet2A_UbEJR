import pytest
from dotenv import load_dotenv

from src.DAO.AddressDAO import AddressDAO
from src.DAO.BundleDAO import BundleDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderableDAO import OrderableDAO
from src.DAO.OrderDAO import OrderDAO

load_dotenv()


@pytest.fixture(scope="session")
def db_connector_test():
    return DBConnector(test=True)


@pytest.fixture(scope="function")
def clean_database(db_connector_test):
    tables = [
        "Deliveries",
        "Order_contents",
        "Bundle_Items",
        "Bundles",
        "Items",
        "Orderables",
        "Orders",
        "Customers",
        "Drivers",
        "Admins",
        "Addresses",
    ]

    for table in tables:
        db_connector_test.sql_query(
            f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE", return_type="none"
        )

    yield db_connector_test


@pytest.fixture
def orderable_dao(db_connector_test):
    return OrderableDAO(db_connector_test)


@pytest.fixture
def item_dao(db_connector_test, orderable_dao):
    return ItemDAO(db_connector_test, orderable_dao)


@pytest.fixture
def bundle_dao(db_connector_test, orderable_dao, item_dao):
    return BundleDAO(db_connector_test, orderable_dao, item_dao)


@pytest.fixture
def order_dao(db_connector_test):
    return OrderDAO(db_connector_test)


@pytest.fixture
def address_dao(db_connector_test):
    return AddressDAO(db_connector_test)


@pytest.fixture
def customer_dao(db_connector_test, address_dao):
    return CustomerDAO(db_connector_test, address_dao)


@pytest.fixture
def sample_address(address_dao, clean_database):
    address = address_dao.create_address(
        number=7,
        street="Contour Antoine de Saint-Exupéry",
        city="Bruz",
        postal_code=35170,
        country="France",
    )
    return address


@pytest.fixture
def sample_customer(customer_dao, sample_address, clean_database):
    customer = customer_dao.create_customer(
        first_name="Jean",
        last_name="Dupont",
        phone="0612345678",
        mail="jean.dupont@email.com",
        password_hash="hashed_password_123",
        salt="random_salt_456",
        address_id=sample_address.address_id,
    )
    return customer


@pytest.fixture
def sample_item_data():
    return {
        "item_name": "Galette-Saucisse",
        "item_price": 4.5,
        "item_type": "Plat",
        "item_description": "La fameuse galette-saucisse de l'EJR",
        "item_stock": 50,
    }


@pytest.fixture
def sample_item(item_dao, clean_database, sample_item_data):
    return item_dao.create_item(**sample_item_data)


@pytest.fixture
def multiple_items(item_dao, clean_database):
    items = []

    item1 = item_dao.create_item(
        item_name="Galette-Saucisse",
        item_price=4.5,
        item_type="Plat",
        item_description="La fameuse galette-saucisse de l'EJR",
        item_stock=50,
    )
    items.append(item1)

    item2 = item_dao.create_item(
        item_name="Coca-Cola 33cl",
        item_price=0.5,
        item_type="Boisson",
        item_description="Canette de Coca-Cola",
        item_stock=100,
    )
    items.append(item2)

    item3 = item_dao.create_item(
        item_name="Tiramisu",
        item_price=2.0,
        item_type="Dessert",
        item_description="Tiramisu-holic",
        item_stock=30,
    )
    items.append(item3)

    return items
