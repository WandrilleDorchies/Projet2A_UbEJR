import pytest


class TestCustomerService:
    def test_get_customer_by_id_exists(self, customer_service, sample_customer, clean_database):
        """Test getting a customer by id"""
        retrieved_customer = customer_service.get_customer_by_id(sample_customer.id)

        assert retrieved_customer is not None
        assert retrieved_customer.id == sample_customer.id
        assert retrieved_customer.first_name == sample_customer.first_name
        assert retrieved_customer.customer_mail == sample_customer.customer_mail

    def test_get_customer_by_id_not_exists(self, customer_service, clean_database):
        """Test getting customer by non-existing id raises error"""
        with pytest.raises(ValueError, match="Cannot find: customer with ID 9999 not found"):
            customer_service.get_customer_by_id(9999)

    def test_get_customer_by_email_exists(self, customer_service, sample_customer, clean_database):
        """Test getting a customer by email"""
        retrieved_customer = customer_service.get_customer_by_email(sample_customer.customer_mail)

        assert retrieved_customer is not None
        assert retrieved_customer.id == sample_customer.id
        assert retrieved_customer.customer_mail == sample_customer.customer_mail

    def test_get_customer_by_email_not_exists(self, customer_service, clean_database):
        """Test getting customer by non-existing email returns None"""
        retrieved_customer = customer_service.get_customer_by_email("nonexistent@email.com")

        assert retrieved_customer is None

    def test_get_customer_by_phone_exists(self, customer_service, sample_customer, clean_database):
        """Test getting a customer by phone"""
        retrieved_customer = customer_service.get_customer_by_phone(sample_customer.customer_phone)

        assert retrieved_customer is not None
        assert retrieved_customer.id == sample_customer.id
        assert retrieved_customer.customer_phone == sample_customer.customer_phone

    def test_get_customer_by_phone_not_exists(self, customer_service, clean_database):
        """Test getting customer by non-existing phone returns None"""
        retrieved_customer = customer_service.get_customer_by_phone("0699999999")

        assert retrieved_customer is None

    def test_get_all_customers_empty(self, customer_service, clean_database):
        """Test getting all customers when there are none"""
        customers = customer_service.get_all_customers()

        assert customers == []

    def test_get_all_customer_multiple(
        self, customer_service, address_dao, customer_dao, clean_database
    ):
        """Test getting all customers"""
        address = address_dao.create_address(1, "Rue Test", "Rennes", 35000, "France")

        customer_dao.create_customer(
            "A", "A", "0601", "a@test.com", "hash", "salt", address.address_id
        )
        customer_dao.create_customer(
            "B", "B", "0602", "b@test.com", "hash", "salt", address.address_id
        )
        customer_dao.create_customer(
            "C", "C", "0603", "c@test.com", "hash", "salt", address.address_id
        )

        customers = customer_service.get_all_customers()

        assert customers != []
        assert len(customers) == 3

    def test_get_all_customer_email(self, customer_service, sample_customer, clean_database):
        """Test getting all customer emails"""
        emails = customer_service.get_all_customer_email()

        assert emails is not None
        assert len(emails) >= 1
        assert sample_customer.customer_mail in emails

    def test_create_customer_success(self, customer_service, clean_database):
        """Test creating a customer successfully"""
        created_customer = customer_service.create_customer(
            first_name="Test",
            last_name="User",
            phone="0612345678",
            mail="test@email.com",
            password="V4lidP@ssword",
            address_string="51 Rue Blaise Pascal, 35170 Bruz, France",
        )

        assert created_customer is not None
        assert created_customer.id > 0
        assert created_customer.first_name == "Test"
        assert created_customer.last_name == "User"
        assert created_customer.customer_phone == "0612345678"
        assert created_customer.customer_mail == "test@email.com"
        assert created_customer.customer_address is not None

    def test_create_customer_duplicate_email_raises_error(
        self, customer_service, sample_customer, clean_database
    ):
        """Test creating customer with duplicate email raises error"""
        with pytest.raises(ValueError, match="already exists"):
            customer_service.create_customer(
                first_name="Test",
                last_name="User",
                phone="0698765432",
                mail=sample_customer.customer_mail,
                password="V4lidP@ssword",
                address_string="51 Rue Blaise Pascal, 35170 Bruz, France",
            )

    def test_create_customer_duplicate_phone_raises_error(
        self, customer_service, sample_customer, clean_database
    ):
        """Test creating customer with duplicate phone raises error"""
        with pytest.raises(ValueError, match="already exists"):
            customer_service.create_customer(
                first_name="Test",
                last_name="User",
                phone=sample_customer.customer_phone,
                mail="newtest@email.com",
                password="V4lidP@ssword",
                address_string="51 Rue Blaise Pascal, 35170 Bruz, France",
            )

    def test_create_customer_weak_password_raises_error(self, customer_service, clean_database):
        """Test creating customer with weak password raises error"""
        with pytest.raises(ValueError):
            customer_service.create_customer(
                first_name="Test",
                last_name="User",
                phone="0612345678",
                mail="test@email.com",
                password="weak",
                address_string="51 Rue Blaise Pascal, 35170 Bruz, France",
            )

    def test_create_customer_invalid_phone_raises_error(self, customer_service, clean_database):
        """Test creating customer with invalid phone raises error"""
        with pytest.raises(ValueError, match="invalid"):
            customer_service.create_customer(
                first_name="Test",
                last_name="User",
                phone="123",
                mail="test@email.com",
                password="V4lidP@ssword",
                address_string="51 Rue Blaise Pascal, 35170 Bruz, France",
            )

    def test_create_customer_invalid_address_raises_error(self, customer_service, clean_database):
        """Test creating customer with invalid address raises error"""
        with pytest.raises(ValueError, match="invalid or outside the delivery zone"):
            customer_service.create_customer(
                first_name="Test",
                last_name="User",
                phone="0612345678",
                mail="test@email.com",
                password="V4lidP@ssword",
                address_string="Invalid Address XYZ",
            )

    def test_create_customer_address_too_far_raises_error(self, customer_service, clean_database):
        """Test creating customer with address too far raises error"""
        with pytest.raises(ValueError, match="invalid or outside the delivery zone"):
            customer_service.create_customer(
                first_name="Test",
                last_name="User",
                phone="0612345678",
                mail="test@email.com",
                password="V4lidP@ssword",
                address_string="Tour Eiffel, 75007 Paris, France",
            )

    def test_update_customer(self, customer_service, sample_customer, clean_database):
        """Test updating a customer"""
        updated_customer = customer_service.update_customer(
            sample_customer.id,
            {
                "customer_first_name": "UpdatedName",
                "customer_last_name": "UpdatedLastName",
            },
        )

        assert updated_customer.first_name == "UpdatedName"
        assert updated_customer.last_name == "UpdatedLastName"
        assert updated_customer.customer_mail == sample_customer.customer_mail

    def test_update_phone(self, customer_service, sample_customer, clean_database):
        """Test updating customer phone"""
        updated_customer = customer_service.update_phone(sample_customer.id, "0687654321")

        assert updated_customer.customer_phone == "0687654321"

    def test_update_phone_invalid_raises_error(
        self, customer_service, sample_customer, clean_database
    ):
        """Test updating with invalid phone raises error"""
        with pytest.raises(ValueError, match="invalid"):
            customer_service.update_phone(sample_customer.id, "123")

    def test_make_order(self, customer_service, sample_customer, clean_database):
        """Test making an order"""
        order = customer_service.make_order(sample_customer.id)

        assert order is not None
        assert order.order_id > 0
        assert order.order_customer_id == sample_customer.id

    def test_order_history_empty(self, customer_service, sample_customer, clean_database):
        """Test getting order history when empty"""
        history = customer_service.order_history(sample_customer.id)

        assert history == []

    def test_order_history_multiple_orders(
        self, customer_service, sample_customer, order_dao, clean_database
    ):
        """Test getting order history with multiple orders"""
        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)
        order_dao.create_order(sample_customer.id)

        history = customer_service.order_history(sample_customer.id)

        assert history is not None
        assert len(history) == 3
        assert all(o.order_customer_id == sample_customer.id for o in history)

    def test_delete_customer(self, customer_service, sample_customer, clean_database):
        """Test deleting a customer"""
        customer_service.delete_customer(sample_customer.id)

        with pytest.raises(ValueError, match="Cannot find: customer with ID .* not found"):
            customer_service.get_customer_by_id(sample_customer.id)

    def test_delete_customer_not_exists_raises_error(self, customer_service, clean_database):
        """Test deleting non-existing customer raises error"""
        with pytest.raises(ValueError, match="Cannot delete: customer with ID 9999 not found"):
            customer_service.delete_customer(9999)
