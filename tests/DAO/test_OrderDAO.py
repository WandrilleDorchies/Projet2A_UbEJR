from src.DAO.DBConnector import DBConnector
from src.DAO.OrderDAO import OrderDAO
from src.Model.Item import Item

from datetime import date, time


def test_get_order_by_id():
    order_dao = OrderDAO(DBConnector(test=True))
    order = order_dao.get_order_by_id(1)

    assert order.order_id == 1
    assert order.order_state == 1
    assert order.order_date == date(2025, 10, 21)
    assert order.order_time == time(12, 30)
    assert order.order_is_paid is True
    assert order.order_is_prepared is True


def test_get_items_of_order():
    order_dao = OrderDAO(DBConnector(test=True))
    items = order_dao._get_items_in_order(1)

    assert list(items)[0] == Item(item_id=1,
                                  item_name='Galette-Saucisse',
                                  item_price=4.5,
                                  item_type='Plat',
                                  item_description='La fameuse galette-saucisse de l''EJR',
                                  item_stock=50,
                                  item_in_menu=True)

    assert list(items)[1] == Item(item_id=2,
                                  item_name='Coca-Cola 33cl',
                                  item_price=0.5,
                                  item_type='Boisson',
                                  item_description='Canette de Coca-Cola',
                                  item_stock=100,
                                  item_in_menu=True)


def test_get_all_order():
    order_dao = OrderDAO(DBConnector(test=True))
    items = order_dao.get_all_orders()

    assert len(items) == 2
    assert items[0].order_id == 1
    assert items[1].order_id == 2


def test_get_item_qty():
    order_dao = OrderDAO(DBConnector(test=True))
    qty = order_dao._get_quantity_of_item(2, 4)

    assert qty == 2


def test_create_order():
    order_dao = OrderDAO(DBConnector(test=True))
    order = order_dao.create_order(3)

    assert order.order_id == 3


def test_update_order():
    pass


def test_delete_order():
    pass


def test_item_from_order():
    pass


def test_remove_item_from_order():
    pass
