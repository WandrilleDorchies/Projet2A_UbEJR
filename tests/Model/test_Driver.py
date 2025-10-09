from datetime import datetime
from unittest.mock import Mock

import pytest
from pydantic_core import ValidationError

from src.Model.Driver import Driver
from src.Model.User import User


class TestDriver:
    """Test suite for the Driver class"""

    def setup_method(self):
        """Setup mock data for each test"""
        self.mock_user_data = {
            "user_id": 1,
            "user_first_name": "Test",
            "user_last_name": "Goat",
            "user_created_at": datetime.now(),
            "user_password": "hashed_password",
            "user_salt": "random_salt"
        }

        self.mock_driver_data = {
            "driver_phone": "0724368754",
            "driver_is_delivering": False
        }

    def _create_driver(self, **overrides):
        """Helper method to create a driver with merged data"""
        data = {**self.mock_user_data, **self.mock_driver_data, **overrides}
        return Driver(**data)

    def test_driver_creation_valid_data(self):
        """Test creating a driver with valid data"""
        driver = self._create_driver()

        assert isinstance(driver, User)
        assert driver.user_id == 1
        assert driver.user_first_name == "Test"
        assert driver.user_last_name == "Goat"
        assert driver.driver_phone == "0724368754"
        assert driver.driver_is_delivering is False
        assert isinstance(driver.user_created_at, datetime)

    def test_driver_creation_with_is_delivering_true(self):
        """Test creating a driver with driver_is_delivering set to True"""
        driver = self._create_driver(driver_is_delivering=True)
        assert driver.driver_is_delivering is True

    def test_driver_creation_missing_phone(self):
        """Test that driver_phone is required for Driver"""
        data = {**self.mock_user_data}  # Only user data, no driver_phone

        with pytest.raises(ValidationError) as exc_info:
            Driver(**data)
        assert "driver_phone" in str(exc_info.value)

    def test_driver_creation_invalid_phone_type(self):
        """Test that driver_phone must be a string"""
        with pytest.raises(ValidationError) as exc_info:
            self._create_driver(driver_phone=1234567890)
        assert "string" in str(exc_info.value).lower()

    def test_driver_creation_phone_empty_string(self):
        """Test that empty string driver_phone raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self._create_driver(driver_phone="")
        assert "driver_phone" in str(exc_info.value).lower()

    def test_driver_creation_phone_whitespace_only(self):
        """Test that whitespace-only driver_phone raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self._create_driver(driver_phone="   ")
        assert "driver_phone" in str(exc_info.value).lower()

    def test_driver_phone_uniqueness_same_format(self):
        """Test that duplicate phone numbers in same format raise error"""
        driver1 = self._create_driver(user_id=1, driver_phone="0724368754")

        with pytest.raises(ValueError, match="Phone number already used"):
            self._check_phone_uniqueness({"driver_phone": "0724368754"}, [driver1])

    def test_driver_phone_uniqueness_different_formats(self):
        """Test that duplicate phone numbers in different formats raise error"""
        driver1 = self._create_driver(user_id=1, driver_phone="0724368754")

        equivalent_phones = [
            "07 24 36 87 54",
            "07-24-36-87-54", 
            "+33724368754",
            "+33 7 24 36 87 54",
            "+33(0)724368754",
        ]

        for phone in equivalent_phones:
            with pytest.raises(ValueError, match="Phone number already used"):
                self._check_phone_uniqueness({"driver_phone": phone}, [driver1])

    def test_driver_phone_uniqueness_multiple_drivers(self):
        """Test phone uniqueness with multiple existing drivers"""
        # Create mock drivers instead of real ones
        existing_drivers = [
            Mock(spec=Driver, driver_phone="0612345678"),
            Mock(spec=Driver, driver_phone="0798765432"), 
            Mock(spec=Driver, driver_phone="0687654321")
        ]

        with pytest.raises(ValueError, match="Phone number already used"):
            self._check_phone_uniqueness({"driver_phone": "07 98 76 54 32"}, existing_drivers)

    def test_driver_phone_unique_valid(self):
        """Test that unique phone numbers don't raise error"""
        existing_drivers = [
            Mock(spec=Driver, driver_phone="0612345678"),
            Mock(spec=Driver, driver_phone="0798765432")
        ]

        # This should not raise an exception
        result = self._check_phone_uniqueness({"driver_phone": "0744556677"}, existing_drivers)
        assert result is True

    def _check_phone_uniqueness(self, new_driver_data, existing_drivers):
        """
        Helper method to check phone uniqueness across drivers.
        This simulates what would happen in a service/repository layer.
        """
        new_phone = new_driver_data["driver_phone"]
        new_phone_normalized = self._normalize_phone(new_phone)

        for existing_driver in existing_drivers:
            existing_phone_normalized = self._normalize_phone(existing_driver.driver_phone)
            if new_phone_normalized == existing_phone_normalized:
                raise ValueError("Phone number already used")

        return True

    def _normalize_phone(self, phone):
        """
        Normalize phone number by removing all non-digit characters except leading +
        This handles different formats of the same phone number.
        """
        if phone.startswith('+'):
            plus = '+'
            digits = ''.join(filter(str.isdigit, phone[1:]))
            if digits.startswith('33'):
                return plus + digits
            elif digits.startswith('0'):
                return plus + '33' + digits[1:]
            else:
                return plus + digits
        else:
            digits = ''.join(filter(str.isdigit, phone))
            if digits.startswith('0'):
                return '+33' + digits[1:]
            else:
                return '+' + digits