#c'est n'importe quoi ce sera modifié
import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import Item


@pytest.fixture
def test_db_connector():
    """Fixture pour le connecteur de base de données de test"""
    return DBConnector(test=True)


@pytest.fixture
def item_dao(test_db_connector):
    """Fixture pour ItemDAO"""
    return ItemDAO(test_db_connector)


