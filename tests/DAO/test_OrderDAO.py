from datetime import date


class TestOrderDAO:
    def test_create_order(self, order_dao, sample_customer, clean_database):
        order = order_dao.create_order(sample_customer.customer_id)

        assert order is not None
        assert order.order_id > 0
        assert order.order_customer_id == sample_customer.customer_id
        assert order.order_state == 0
        assert order.order_date == date.today()
        assert order.order_is_paid is False
        assert order.order_is_prepared is False
        assert order.order_items == {} or order.order_items is None

    def test_get_order_by_id_exists(self, order_dao, sample_customer, clean_database):
        created_order = order_dao.create_order(sample_customer.customer_id)

        retrieved_order = order_dao.get_order_by_id(created_order.order_id)

        assert retrieved_order is not None
        assert retrieved_order.order_id == created_order.order_id
        assert retrieved_order.order_customer_id == sample_customer.customer_id

    def test_get_order_by_id_not_exists(self, order_dao, clean_database):
        retrieved_order = order_dao.get_order_by_id(9999)

        assert retrieved_order is None

    def test_get_all_orders_empty(self, order_dao, clean_database):
        orders = order_dao.get_all_orders()

        assert orders is None or orders == []

    def test_get_all_orders_multiple(self, order_dao, sample_customer, clean_database):
        order_dao.create_order(sample_customer.customer_id)
        order_dao.create_order(sample_customer.customer_id)
        order_dao.create_order(sample_customer.customer_id)

        orders = order_dao.get_all_orders()

        assert orders is not None
        assert len(orders) == 3
        assert all(order.order_customer_id == sample_customer.customer_id for order in orders)

    def test_update_order_payment_status(self, order_dao, sample_customer, clean_database):
        created_order = order_dao.create_order(sample_customer.customer_id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id, is_paid=True, is_prepared=False
        )

        assert updated_order.order_is_paid is True
        assert updated_order.order_is_prepared is False

    def test_update_order_preparation_status(self, order_dao, sample_customer, clean_database):
        created_order = order_dao.create_order(sample_customer.customer_id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id, is_paid=True, is_prepared=True
        )

        assert updated_order.order_is_paid is True
        assert updated_order.order_is_prepared is True

    def test_update_order_both_statuses(self, order_dao, sample_customer, clean_database):
        created_order = order_dao.create_order(sample_customer.customer_id)

        updated_order = order_dao.update_order(
            order_id=created_order.order_id, is_paid=True, is_prepared=True
        )

        assert updated_order.order_is_paid is True
        assert updated_order.order_is_prepared is True

        retrieved_order = order_dao.get_order_by_id(created_order.order_id)
        assert retrieved_order.order_is_paid is True
        assert retrieved_order.order_is_prepared is True
