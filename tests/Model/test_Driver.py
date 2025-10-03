from datetime import datetime

import pytest
from pydantic_core import ValidationError

from src.Model.Driver import Driver
from src.Model.User import User


class TestDriver:
    """Test suite for the Driver class"""

    def test_driver_creation_valid_data(self):
        """Test creating a driver with valid data"""
        driver_data = {
            "id": 1,
            "first_name": "Neo",
            "last_name": "John",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "phone": "0724368754"
        }

        driver = Driver(**driver_data)

        # Verify that Driver is a subclass of User
        assert isinstance(driver, User)
        assert driver.id == 1
        assert driver.first_name == "Neo"
        assert driver.last_name == "John"
        assert driver.phone == "0724368754"
        assert driver.is_delivering is False
        assert isinstance(driver.created_at, datetime)
        assert driver.password == "hashed_password"
        assert driver.salt == "random_salt"

        # Verify that all User attributes are accessible
        assert hasattr(driver, 'id')
        assert hasattr(driver, 'first_name')
        assert hasattr(driver, 'last_name')
        assert hasattr(driver, 'created_at')
        assert hasattr(driver, 'password')
        assert hasattr(driver, 'salt')

    def test_driver_creation_with_is_delivering_true(self):
        """Test creating a driver with is_delivering set to True"""
        driver_data = {
            "id": 2,
            "first_name": "Wandrille",
            "last_name": "Smith",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "phone": "07 85 54 54 65",
            "is_delivering": True
        }

        driver = Driver(**driver_data)

        assert driver.is_delivering is True

    def test_driver_creation_missing_phone(self):
        """Test that phone is required for Driver"""
        driver_data = {
            "id": 3,
            "first_name": "Chahid",
            "last_name": "Wilson",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt"
            # phone is missing
        }

        with pytest.raises(ValidationError) as exc_info:
            Driver(**driver_data)

        assert "phone" in str(exc_info.value)

    def test_driver_creation_invalid_phone_type(self):
        """Test that phone must be a string"""
        driver_data = {
            "id": 4,
            "first_name": "Martin",
            "last_name": "Brown",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "phone": 1234567890  # phone as int instead of str
        }

        with pytest.raises(ValidationError) as exc_info:
            Driver(**driver_data)

        assert "string" in str(exc_info.value).lower()

    def test_driver_creation_phone_empty_string(self):
        """Test that empty string phone raises ValidationError"""
        driver_data = {
            "id": 5,
            "first_name": "Emma",
            "last_name": "Evans",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "phone": ""  # empty string
        }

        with pytest.raises(ValidationError) as exc_info:
            Driver(**driver_data)

        # Check that the error comes from the phone number
        assert "phone" in str(exc_info.value).lower()

    def test_driver_creation_phone_whitespace_only(self):
        """Test that whitespace-only phone raises ValidationError"""
        driver_data = {
            "id": 6,
            "first_name": "Neo",
            "last_name": "Dubois",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "phone": "   "  # whitespace only
        }

        with pytest.raises(ValidationError) as exc_info:
            Driver(**driver_data)

        # Check that the error comes from the phone number
        assert "phone" in str(exc_info.value).lower()

    def test_driver_phone_uniqueness_same_format(self):
        """Test that duplicate phone numbers in same format raise error"""
        # first driver
        driver1_data = {
            "id": 7,
            "first_name": "Wandrille",
            "last_name": "A",
            "created_at": datetime.now(),
            "password": "hashed_password1",
            "salt": "salt1",
            "phone": "0724368754"
        }

        driver1 = Driver(**driver1_data)

        #attempt to create a second driver with the same phone number
        driver2_data = {
            "id": 8,
            "first_name": "Martin",
            "last_name": "B",
            "created_at": datetime.now(),
            "password": "hashed_password2",
            "salt": "salt2",
            "phone": "0724368754"  #Same phone number
        }

        # Check the creation raises an error
        with pytest.raises(ValueError, match="Phone number already used"):
            self._check_phone_uniqueness(driver2_data, [driver1])

    def test_driver_phone_uniqueness_different_formats(self):
        """Test that duplicate phone numbers in different formats raise error"""
        # first driver with a standard phone number format
        driver1_data = {
            "id": 9,
            "first_name": "Neo",
            "last_name": "C",
            "created_at": datetime.now(),
            "password": "hashed_password1",
            "salt": "salt1",
            "phone": "0724368754"
        }

        driver1 = Driver(**driver1_data)

        #Test with different formats representing the same phone number
        equivalent_phones = [
            "07 24 36 87 54",
            "07-24-36-87-54",
            "+33724368754",
            "+33 7 24 36 87 54",
            "+33(0)724368754",
        ]

        for i, phone in enumerate(equivalent_phones):
            driver_data = {
                "id": 10 + i,
                "first_name": f"Duplicate{i}",
                "last_name": "D",
                "created_at": datetime.now(),
                "password": f"hashed_password{i}",
                "salt": f"salt{i}",
                "phone": phone
            }

            #Check that every format raises an error
            with pytest.raises(ValueError, match="Phone number already used"):
                self._check_phone_uniqueness(driver_data, [driver1])

    def test_driver_phone_uniqueness_multiple_drivers(self):
        """Test phone uniqueness with multiple existing drivers"""
        # Créer plusieurs drivers avec des numéros différents
        existing_drivers = []
        phones = ["0612345678", "0798765432", "0687654321"]

        for i, phone in enumerate(phones):
            driver_data = {
                "id": 20 + i,
                "first_name": f"Existing{i}",
                "last_name": "Driver",
                "created_at": datetime.now(),
                "password": f"hash{i}",
                "salt": f"salt{i}",
                "phone": phone
            }
            existing_drivers.append(Driver(**driver_data))

        # Tenter de créer un driver avec un numéro existant
        duplicate_data = {
            "id": 30,
            "first_name": "New",
            "last_name": "Driver",
            "created_at": datetime.now(),
            "password": "new_hash",
            "salt": "new_salt",
            "phone": "07 98 76 54 32"  # Même que "0798765432" mais avec espaces
        }

        with pytest.raises(ValueError, match="Phone number already used"):
            self._check_phone_uniqueness(duplicate_data, existing_drivers)

    def _check_phone_uniqueness(self, new_driver_data, existing_drivers):
        """
        Helper method to check phone uniqueness across drivers.
        This simulates what would happen in a service/repository layer.
        """
        new_phone = new_driver_data["phone"]
        new_phone_normalized = self._normalize_phone(new_phone)

        for existing_driver in existing_drivers:
            existing_phone_normalized = self._normalize_phone(existing_driver.phone)
            if new_phone_normalized == existing_phone_normalized:
                raise ValueError("Phone number already used")

        # If we arrive here, the phone number is unique
        return True

    def _normalize_phone(self, phone):
        """
        Normalize phone number by removing all non-digit characters except leading +
        This handles different formats of the same phone number.
        """
        if phone.startswith('+'):
            # Keep the inital + and keep only figures
            plus = '+'
            digits = ''.join(filter(str.isdigit, phone[1:]))
            # for french phone numbers we normalizes +33
            if digits.startswith('33'):
                return plus + digits
            elif digits.startswith('0'):
                return plus + '33' + digits[1:]
            else:
                return plus + digits
        else:
            # for phone numbers whithout +, we delete every non-figures
            digits = ''.join(filter(str.isdigit, phone))
            if digits.startswith('0'):
                return '+33' + digits[1:]
            else:
                return '+' + digits
