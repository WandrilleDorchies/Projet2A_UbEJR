from datetime import datetime

import pytest


class TestMenuService:
    def test_get_all_orderable_in_menu_empty(self, menu_service, clean_database):
        """Test getting all orderables in menu when menu is empty"""
        orderables = menu_service.get_all_orderables()

        assert orderables == []

    def test_get_all_orderable_in_menu_items_only(
        self, menu_service, multiple_items, clean_database
    ):
        """Test getting all orderables in menu with only items"""
        orderables = menu_service.get_all_orderables()

        assert orderables is not None
        assert len(orderables) == 3
        assert all(o.orderable_type == "item" for o in orderables)

    def test_get_all_orderable_in_menu_mixed(
        self, menu_service, sample_bundle, multiple_items, clean_database
    ):
        """Test getting all orderables in menu with items and bundles"""
        orderables = menu_service.get_all_orderables()
        assert orderables is not None
        assert len(orderables) == 4
        types = [o.orderable_type for o in orderables]
        assert "item" in types
        assert "bundle" in types

    def test_add_orderable_to_menu_item(self, menu_service, item_dao, clean_database):
        """Test adding an item to the menu"""
        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Drink",
            item_description="Item de test",
            item_stock=10,
            is_in_menu=False,
        )

        returned_item = menu_service.add_orderable_to_menu(item.orderable_id)

        assert returned_item is not None
        assert returned_item.orderable_id == item.orderable_id
        assert returned_item.is_in_menu is True

    def test_add_orderable_to_menu_bundle(
        self, menu_service, bundle_dao, multiple_items, clean_database
    ):
        """Test adding a bundle to the menu"""

        bundle_items = {multiple_items[0]: 1}
        bundle = bundle_dao.create_bundle(
            bundle_name="Test Bundle",
            bundle_reduction=10,
            bundle_description="Bundle de test",
            bundle_availability_start_date=datetime(2025, 1, 1),
            bundle_availability_end_date=datetime(2025, 12, 31),
            bundle_items=bundle_items,
            is_in_menu=False,
        )

        returned_bundle = menu_service.add_orderable_to_menu(bundle.orderable_id)

        assert returned_bundle is not None
        assert returned_bundle.orderable_id == bundle.orderable_id
        assert returned_bundle.is_in_menu is True

    def test_add_orderable_to_menu_already_in_menu_raises_error(
        self, menu_service, sample_item, clean_database
    ):
        """Test adding an orderable already in menu raises error"""
        with pytest.raises(ValueError, match="already on the menu"):
            menu_service.add_orderable_to_menu(sample_item.orderable_id)

    def test_add_orderable_to_menu_not_exists_raises_error(self, menu_service, clean_database):
        """Test adding non-existing orderable raises error"""
        with pytest.raises(ValueError, match="unknown"):
            menu_service.add_orderable_to_menu(9999)

    def test_remove_orderable_from_menu_item(self, menu_service, sample_item, clean_database):
        """Test removing an item from the menu"""
        returned_item = menu_service.remove_orderable_from_menu(sample_item.orderable_id)

        assert returned_item is not None
        assert returned_item.orderable_id == sample_item.orderable_id
        assert returned_item.is_in_menu is False

    def test_remove_orderable_from_menu_bundle(self, menu_service, sample_bundle, clean_database):
        """Test removing a bundle from the menu"""
        returned_bundle = menu_service.remove_orderable_from_menu(sample_bundle.orderable_id)

        assert returned_bundle is not None
        assert returned_bundle.orderable_id == sample_bundle.orderable_id
        assert returned_bundle.is_in_menu is False

    def test_remove_orderable_from_menu_already_off_menu_raises_error(
        self, menu_service, item_dao, clean_database
    ):
        """Test removing an orderable already off menu raises error"""
        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Drink",
            item_description="Item de test",
            item_stock=10,
            is_in_menu=False,
        )

        with pytest.raises(ValueError, match="already off the menu"):
            menu_service.remove_orderable_from_menu(item.orderable_id)

    def test_remove_orderable_from_menu_not_exists_raises_error(self, menu_service, clean_database):
        """Test removing non-existing orderable raises error"""
        with pytest.raises(ValueError, match="unknown"):
            menu_service.remove_orderable_from_menu(9999)

    def test_add_then_remove_orderable(self, menu_service, item_dao, clean_database):
        """Test adding then removing an orderable from menu"""
        item = item_dao.create_item(
            item_name="Test Item",
            item_price=5.0,
            item_type="Drink",
            item_description="Item de test",
            item_stock=10,
            is_in_menu=False,
        )

        menu_service.add_orderable_to_menu(item.orderable_id)
        orderables = menu_service.get_all_orderables()
        assert any(o.orderable_id == item.orderable_id for o in orderables)

        menu_service.remove_orderable_from_menu(item.orderable_id)
        orderables = menu_service.get_all_orderables()
        assert not any(o.orderable_id == item.orderable_id for o in orderables)
