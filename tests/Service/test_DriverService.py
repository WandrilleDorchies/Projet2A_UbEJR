import re

import pytest


class TestDriverService:
    def test_get_driver_by_id_exists(self, driver_service, sample_driver, clean_database):
        """Test getting a driver by id"""
        retrieved_driver = driver_service.get_driver_by_id(sample_driver.id)

        assert retrieved_driver is not None
        assert retrieved_driver.id == sample_driver.id
        assert retrieved_driver.first_name == sample_driver.first_name

    def test_get_driver_by_phone(self, driver_service, sample_driver, clean_database):
        """Test getting a driver by phone"""
        retrieved_driver = driver_service.get_driver_by_phone(sample_driver.driver_phone)

        assert retrieved_driver is not None
        assert retrieved_driver.id == sample_driver.id
        assert retrieved_driver.first_name == sample_driver.first_name

    def test_get_driver_by_phone_not_exists(self, driver_service, sample_driver, clean_database):
        """Test getting a driver by non-existing phone"""
        with pytest.raises(
            ValueError,
            match=re.escape(
                "[DriverService] Cannot update driver: "
                "driver with phone mental breakdown not found."
            ),
        ):
            driver_service.get_driver_by_phone("mental breakdown")

    def test_get_driver_by_id_not_exists(self, driver_service, clean_database):
        """Test getting driver by non-existing id raises error"""
        with pytest.raises(ValueError, match="Cannot update driver: driver with ID 9999 not found"):
            driver_service.get_driver_by_id(9999)

    def test_get_all_driver_empty(self, driver_service, clean_database):
        """Test getting all drivers when there are none"""
        drivers = driver_service.get_all_driver()

        assert drivers == []

    def test_get_all_driver_multiple(self, driver_service, driver_dao, clean_database):
        """Test getting all drivers"""
        driver_dao.create_driver("A", "A", "0701", "hash", "salt")
        driver_dao.create_driver("B", "B", "0702", "hash", "salt")
        driver_dao.create_driver("C", "C", "0703", "hash", "salt")

        drivers = driver_service.get_all_driver()

        assert drivers is not None
        assert len(drivers) == 3

    def test_create_driver(self, driver_service, clean_database):
        """Test creating a driver"""
        created_driver = driver_service.create_driver(
            first_name="Test",
            last_name="Driver",
            phone="0612345678",
            password="V4lidP@ssword",
        )

        assert created_driver is not None
        assert created_driver.id == 1
        assert created_driver.first_name == "Test"
        assert created_driver.last_name == "Driver"
        assert created_driver.driver_is_delivering is False

    def test_update_driver(self, driver_service, sample_driver, clean_database):
        """Test updating a driver"""
        updated_driver = driver_service.update_driver(
            sample_driver.id, {"driver_first_name": "UpdatedName", "driver_is_delivering": True}
        )

        assert updated_driver.first_name == "UpdatedName"
        assert updated_driver.driver_is_delivering is True

    def test_update_driver_not_exists(self, driver_service, clean_database):
        """Test updating non-existing driver raises error"""
        with pytest.raises(ValueError, match="Cannot update driver: driver with ID 9999 not found"):
            driver_service.update_driver(9999, {"driver_first_name": "Test"})

    def test_accept_order(
        self, driver_service, sample_order, sample_driver, clean_database, delivery_dao
    ):
        """Test accepting an order"""
        delivery = driver_service.accept_order(sample_order.order_id, sample_driver.id)

        assert delivery is not None
        assert delivery.delivery_order_id == sample_order.order_id
        assert delivery.delivery_driver_id == sample_driver.id
        assert delivery.delivery_state == 0

    def test_accept_order_driver_not_exists(self, driver_service, sample_order, clean_database):
        """Test accepting order with non-existing driver raises error"""
        with pytest.raises(ValueError, match="Cannot accept order: driver with ID 9999 not found"):
            driver_service.accept_order(sample_order.order_id, 9999)

    def test_delivery_start(
        self, driver_service, sample_order, sample_driver, clean_database, delivery_dao
    ):
        """Test starting a delivery"""
        delivery_dao.create_delivery(sample_order.order_id, sample_driver.id)

        updated_delivery = driver_service.delivery_start(sample_order.order_id, sample_driver.id)

        assert updated_delivery.delivery_state == 1

        updated_driver = driver_service.get_driver_by_id(sample_driver.id)
        assert updated_driver.driver_is_delivering is True

    def test_delivery_start_driver_not_exists(self, driver_service, sample_order, clean_database):
        """Test starting delivery with non-existing driver raises error"""
        with pytest.raises(
            ValueError, match="Cannot start delivery: driver with ID 9999 not found"
        ):
            driver_service.delivery_start(sample_order.order_id, 9999)

    def test_delivery_end(
        self, driver_service, sample_order, sample_driver, clean_database, delivery_dao
    ):
        """Test ending a delivery"""
        delivery_dao.create_delivery(sample_order.order_id, sample_driver.id)
        driver_service.delivery_start(sample_order.order_id, sample_driver.id)

        updated_delivery = driver_service.delivery_end(sample_order.order_id, sample_driver.id)

        assert updated_delivery.delivery_state == 2

        updated_driver = driver_service.get_driver_by_id(sample_driver.id)
        assert updated_driver.driver_is_delivering is False

    def test_delivery_end_driver_not_exists(self, driver_service, sample_order, clean_database):
        """Test ending delivery with non-existing driver raises error"""
        with pytest.raises(ValueError, match="Cannot end delivery: driver with ID 9999 not found"):
            driver_service.delivery_end(sample_order.order_id, 9999)

    def test_delete_driver(self, driver_service, sample_driver, clean_database):
        """Test deleting a driver"""
        driver_service.delete_driver(sample_driver.id)

        with pytest.raises(ValueError, match="Cannot update driver: driver with ID .* not found"):
            driver_service.get_driver_by_id(sample_driver.id)

    def test_delete_driver_not_exists(self, driver_service, clean_database):
        """Test deleting non-existing driver raises error"""
        with pytest.raises(ValueError, match="Cannot delete: driver with ID 9999 not found"):
            driver_service.delete_driver(9999)
