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


@pytest.fixture
def sample_item_data():
    """Fixture avec des données d'item exemple"""
    return {
        "item_id": 1,
        "item_name": "Galette-Saucisse",
        "item_price": 4.5,
        "item_type": "Plat",
        "item_description": "La fameuse galette-saucisse de l'EJR",
        "item_stock": 50,
        "item_in_menu": True
    }


@pytest.fixture
def sample_item_2_data():
    """Fixture avec un deuxième item exemple"""
    return {
        "item_id": 2,
        "item_name": "Coca-Cola 33cl",
        "item_price": 0.5,
        "item_type": "Boisson",
        "item_description": "Canette de Coca-Cola",
        "item_stock": 100,
        "item_in_menu": True
    }


@pytest.fixture
def sample_item_instance(sample_item_data):
    """Fixture qui crée une instance d'Item"""
    return Item(**sample_item_data)


def test_create_item(item_dao, sample_item_data):
    """Test la création d'un item"""
    # Utilise les données de la fixture pour créer l'item
    item = item_dao.create_item(
        item_id=sample_item_data["item_id"],
        item_name=sample_item_data["item_name"],
        item_price=sample_item_data["item_price"],
        item_type=sample_item_data["item_type"],
        item_description=sample_item_data["item_description"],
        item_stock=sample_item_data["item_stock"]
    )
    
    # Vérifications
    assert isinstance(item, Item)
    assert item.item_id == sample_item_data["item_id"]
    assert item.item_name == sample_item_data["item_name"]
    assert item.item_price == sample_item_data["item_price"]
    assert item.item_type == sample_item_data["item_type"]
    assert item.item_description == sample_item_data["item_description"]
    assert item.item_stock == sample_item_data["item_stock"]
    assert item.item_in_menu == sample_item_data["item_in_menu"]


def test_get_item_by_id_found(item_dao, sample_item_instance):
    """Test la récupération d'un item par son ID quand il existe"""
    # Récupère l'item depuis la base (supposant qu'il existe avec ID 1)
    item = item_dao.get_item_by_id(1)
    
    # Vérifications
    assert isinstance(item, Item)
    assert item.item_id == 1
    # On peut vérifier d'autres attributs selon les données de test dans la base


def test_get_item_by_id_not_found(item_dao):
    """Test la récupération d'un item par son ID quand il n'existe pas"""
    # Tente de récupérer un item avec un ID qui n'existe pas
    item = item_dao.get_item_by_id(999)
    
    # Vérifie que None est retourné
    assert item is None


def test_get_all_items(item_dao):
    """Test la récupération de tous les items"""
    items = item_dao.get_all_items()
    
    # Vérifications
    assert items is not None
    assert isinstance(items, list)
    assert all(isinstance(item, Item) for item in items)
    
    # Vérifie qu'on a au moins un item (selon les données de test)
    assert len(items) >= 1


def test_get_all_items_empty(item_dao):
    """Test la récupération quand il n'y a pas d'items"""
    # Cette test pourrait nécessiter une base vide
    # Pour l'instant, on vérifie juste que la méthode ne crash pas
    items = item_dao.get_all_items()
    
    # La méthode peut retourner None ou une liste vide selon l'implémentation
    assert items is None or isinstance(items, list)


def test_delete_item_by_id(item_dao):
    """Test la suppression d'un item par son ID"""
    # Crée d'abord un item pour le supprimer
    new_item = item_dao.create_item(
        item_id=100,
        item_name="Item à supprimer",
        item_price=10.0,
        item_type="Test",
        item_description="Item créé pour test de suppression",
        item_stock=5
    )
    
    # Supprime l'item
    item_dao.delete_item_by_id(100)
    
    # Vérifie que l'item n'existe plus
    deleted_item = item_dao.get_item_by_id(100)
    assert deleted_item is None


def test_singleton_pattern(test_db_connector):
    """Test que ItemDAO suit le pattern singleton"""
    item_dao1 = ItemDAO(test_db_connector)
    item_dao2 = ItemDAO(test_db_connector)
    
    # Vérifie que les deux références pointent vers la même instance
    assert item_dao1 is item_dao2


def test_item_creation_with_different_data(item_dao):
    """Test la création d'items avec différentes données"""
    # Test avec un item de type Entrée
    entree_item = item_dao.create_item(
        item_id=3,
        item_name="Salade Bretonne",
        item_price=8.5,
        item_type="Entrée",
        item_description="Salade avec des produits bretons",
        item_stock=25
    )
    
    assert entree_item.item_id == 3
    assert entree_item.item_name == "Salade Bretonne"
    assert entree_item.item_price == 8.5
    assert entree_item.item_type == "Entrée"
    assert entree_item.item_stock == 25
    
    # Test avec un item hors menu
    hors_menu_item = item_dao.create_item(
        item_id=4,
        item_name="Spéciale du Chef",
        item_price=15.0,
        item_type="Plat",
        item_description="Plat spécial non disponible en menu",
        item_stock=10
    )
    
    assert hors_menu_item.item_id == 4
    assert hors_menu_item.item_name == "Spéciale du Chef"
    assert hors_menu_item.item_price == 15.0
    assert hors_menu_item.item_stock == 10


def test_item_integration_flow(item_dao):
    """Test un flux complet de création, récupération et suppression d'item"""
    # Crée un nouvel item
    new_item = item_dao.create_item(
        item_id=200,
        item_name="Test Integration",
        item_price=12.5,
        item_type="Dessert",
        item_description="Item de test pour flux d'intégration",
        item_stock=30
    )
    
    # Vérifie que l'item a été créé
    assert new_item.item_id == 200
    assert new_item.item_name == "Test Integration"
    
    # Récupère l'item par son ID
    retrieved_item = item_dao.get_item_by_id(200)
    assert retrieved_item is not None
    assert retrieved_item.item_id == 200
    assert retrieved_item.item_name == "Test Integration"
    
    # Vérifie que l'item apparaît dans la liste de tous les items
    all_items = item_dao.get_all_items()
    item_ids = [item.item_id for item in all_items] if all_items else []
    assert 200 in item_ids
    
    # Supprime l'item
    item_dao.delete_item_by_id(200)
    
    # Vérifie que l'item a été supprimé
    deleted_item = item_dao.get_item_by_id(200)
    assert deleted_item is None