from datetime import date, datetime

import pytest


class TestOrderDAO:
    def test_create_order(self, order_dao, sample_customer, clean_database):
        """Test creation of an order"""
        order = order_dao.create_order(sample_customer.id)

        assert order is not None
        assert order.order_id > 0
        assert order.order_customer_id == sample_customer.id
        assert order.order_state == 0
        assert order.order_date == date.today()
        assert order.order_is_paid is False
        assert order.order_is_prepared is False
        assert order.order_items == {} or order.order_items is None

    def test_get_order_by_id_exists(self, order_dao, sample_customer, clean_database):
        """Test get an order by id"""
        created_order = order_dao.create_order(sample_customer.id)

        retrieved_order = order_dao.get_order_by_id(created_order.order_id)

        assert retrieved_order is not None
        assert retrieved_order.order_id == created_order.order_id
        assert retrieved_order.order_customer_id == sample_customer.id

    def test_get_order_by_id_not_exists(self, order_dao, clean_database):
        """Test get an order by id that doesn't exists"""
        retrieved_order = order_dao.get_order_by_id(9999)

        assert retrieved_order is None

    def test_get_all_orders_empty(self, order_dao, clean_database):
        """Tests that get_all_orders returns None"""
        orders = order_dao.get_all_orders()

        assert orders is None

    def test_get_all_orders_multiple(self, order_dao, sample_customer, clean_database):
        """Tests that get_all_orders returns all the orders"""
        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)

        orders = order_dao.get_all_orders()

        assert orders is not None
        assert len(orders) == 3
        assert all(order.order_customer_id == sample_customer.id for order in orders)

    def test_get_all_orders_by_customer_exists(self, order_dao, sample_customer, clean_database):
        """Test fetching all orders of an existing customer"""
        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)

        orders = order_dao.get_all_orders_by_customer(sample_customer.id)

        assert orders is not None
        assert len(orders) == 2
        assert all(o.order_customer_id == sample_customer.id for o in orders)

    def test_get_all_orders_by_customer_not_exists(self, order_dao, clean_database):
        """Test fetching all orders of a non-existing customer"""
        orders = order_dao.get_all_orders_by_customer(9999)

        assert orders is None

    def test_get_all_orders_prepared(self, order_dao, sample_customer, clean_database):
        """Test fetching all prepared orders"""

        order1 = order_dao.create_order(sample_customer.id)
        order2 = order_dao.create_order(sample_customer.id)
        order3 = order_dao.create_order(sample_customer.id)

        order_dao.update_order(order1.order_id, {"order_is_prepared": True})
        order_dao.update_order(order2.order_id, {"order_is_prepared": False})
        order_dao.update_order(order3.order_id, {"order_is_prepared": True})

        prepared_orders = order_dao.get_all_orders_prepared()

        assert prepared_orders is not None
        assert len(prepared_orders) == 2
        assert all(o.order_is_prepared is True for o in prepared_orders)

    def test_no_orders_prepared(self, order_dao, sample_customer, clean_database):
        """Test fetching orders prepared when there is no orders prepared"""

        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)

        prepared_orders = order_dao.get_all_orders_prepared()

        assert prepared_orders is None

    def test_update_order_payment_status(self, order_dao, sample_customer, clean_database):
        """Test updating payment status"""
        created_order = order_dao.create_order(sample_customer.id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id, update={"order_is_paid": True}
        )

        assert updated_order.order_is_paid is True
        assert updated_order.order_is_prepared is False

    def test_update_order_preparation_status(self, order_dao, sample_customer, clean_database):
        """Test updating preparation status"""
        created_order = order_dao.create_order(sample_customer.id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id, update={"order_is_prepared": True}
        )

        assert updated_order.order_is_prepared is True
        assert updated_order.order_is_paid is False

    def test_update_order_state(self, order_dao, sample_customer, clean_database):
        """Test updating order state"""
        created_order = order_dao.create_order(sample_customer.id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id, update={"order_state": 2}
        )

        assert updated_order.order_state == 2

    def test_update_order_all_fields(self, order_dao, sample_customer, clean_database):
        """Test updating all fields at once"""
        created_order = order_dao.create_order(sample_customer.id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id,
            update={"order_is_paid": True, "order_is_prepared": True, "order_state": 3},
        )

        assert updated_order.order_is_paid is True
        assert updated_order.order_is_prepared is True
        assert updated_order.order_state == 3

    def test_update_order_empty_dict_raises_error(self, order_dao, sample_customer, clean_database):
        """Test updating with empty dictionnary"""
        created_order = order_dao.create_order(sample_customer.id)

        with pytest.raises(ValueError, match="At least one value should be updated"):
            order_dao.update_order(created_order.order_id, {})

    def test_update_order_invalid_field_raises_error(
        self, order_dao, sample_customer, clean_database
    ):
        """Test updating with wrong field"""
        created_order = order_dao.create_order(sample_customer.id)

        with pytest.raises(ValueError, match="not a parameter of Order"):
            order_dao.update_order(created_order.order_id, {"invalid_field": "value"})

    def test_delete_order(self, order_dao, sample_customer, clean_database):
        """Test deleting order"""
        created_order = order_dao.create_order(sample_customer.id)
        order_id = created_order.order_id

        order_dao.delete_order(order_id)

        retrieved_order = order_dao.get_order_by_id(order_id)
        assert retrieved_order is None

    def test_delete_order_cascade_order_contents(
        self, order_dao, sample_customer, item_dao, bundle_dao, orderable_dao, clean_database
    ):
        """Test that deleting order deletes it from Order_contents table"""
        order = order_dao.create_order(sample_customer.id)

        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Test",
            item_description="Item de test",
            item_stock=10,
        )
        order_dao.add_orderable_to_order(order.order_id, item.orderable_id)

        bundle = bundle_dao.create_bundle(
            bundle_name="Test Bundle",
            bundle_reduction=5,
            bundle_description="Test",
            bundle_availability_start_date=datetime(2025, 10, 9),
            bundle_availability_end_date=datetime(2026, 10, 9),
            bundle_items={item: 2},
        )
        order_dao.add_orderable_to_order(order.order_id, bundle.orderable_id)

        order_dao.delete_order(order.order_id)

        retrieved_order = order_dao.get_order_by_id(order.order_id)
        assert retrieved_order is None

    def test_add_orderable_to_order_new(
        self, order_dao, item_dao, sample_customer, clean_database, orderable_dao
    ):
        """Test adding an item for the first time"""

        order = order_dao.create_order(sample_customer.id)

        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Test",
            item_description="Item de test",
            item_stock=10,
        )
        updated_order = order_dao.add_orderable_to_order(order.order_id, item.orderable_id)

        assert updated_order is not None
        assert len(updated_order.order_items) == 1

    def test_add_orderable_to_order_increment(
        self, order_dao, item_dao, sample_customer, clean_database, orderable_dao
    ):
        """Test adding an item multiple times"""

        order = order_dao.create_order(sample_customer.id)

        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Test",
            item_description="Item de test",
            item_stock=10,
        )
        order = order_dao.add_orderable_to_order(order.order_id, item.orderable_id)
        order = order_dao.add_orderable_to_order(order.order_id, item.orderable_id)

        quantity = order_dao._get_quantity_of_orderables(order.order_id, item.orderable_id)
        assert quantity == 2
        assert list(order.order_items.keys())[0] == item

    def test_remove_orderable_from_order_decrement(
        self, order_dao, item_dao, sample_customer, clean_database, orderable_dao
    ):
        """Test removing item"""

        order = order_dao.create_order(sample_customer.id)

        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Test",
            item_description="Item de test",
            item_stock=10,
        )

        order_dao.add_orderable_to_order(item.orderable_id, order.order_id)
        order_dao.add_orderable_to_order(item.orderable_id, order.order_id)

        updated_order = order_dao.remove_orderable_from_order(order.order_id, item.orderable_id)

        assert updated_order is not None

    def test_remove_orderable_from_order_delete(
        self, order_dao, item_dao, sample_customer, clean_database, orderable_dao
    ):
        """Test removing all occurences of an item"""
        order = order_dao.create_order(sample_customer.id)

        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Test",
            item_description="Item de test",
            item_stock=10,
        )
        order_dao.add_orderable_to_order(item.orderable_id, order.order_id)

        order_dao.remove_orderable_from_order(order.order_id, item.orderable_id)

        quantity = order_dao._get_quantity_of_orderables(order.order_id, item.orderable_id)
        assert quantity == 0
