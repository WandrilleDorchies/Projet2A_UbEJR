#NOT FINISHED PLS DO NOT TOUCH 
from datetime import datetime

import pytest
from pydantic_core import ValidationError

from src.Model.Address import Address
from src.Model.Customer import Customer
from src.Model.User import User


class TestCustomer:
    """Test for the Customer class"""

    def test_customer_creation_valid_data(self):
        """Test creating a customer with valid data"""
        address = Address(
            street_number="123",
            street_name="Main Street",
            postal_code="75001",
            city="Paris",
            country="France"
        )

        customer_data = {
            "id": 1,
            "first_name": "Martin",
            "last_name": "Matin",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "address": address,
            "phone": "0724368754",
            "mail": "alice.martin@gmail.com"
        }

        customer = Customer(**customer_data)

        assert isinstance(customer, User)
        assert customer.id == 1
        assert customer.first_name == "Martin"
        assert customer.last_name == "Matin"
        assert customer.phone == "0724368754"
        assert customer.mail == "alice.martin@gmail.com"
        assert customer.address == address

    def test_customer_creation_with_valid_domains(self):
        """Test creating a customer with all valid email domains"""
        address = Address(
            street_number="456",
            street_name="Oak Avenue",
            postal_code="69002",
            city="Lyon",
            country="France"
        )

        valid_domains = [
            "gmail.com",
            "free.fr",
            "hotmail.fr",
            "hotmail.com",
            "yahoo.fr",
            "laposte.net",
            "orange.fr",
            "ena.fr",
            "wanadoo.fr",
            "eleve.ensai.fr",
            "insee.fr"
        ]

        for i, domain in enumerate(valid_domains):
            customer_data = {
                "id": 100 + i,
                "first_name": f"Test{i}",
                "last_name": "Customer",
                "created_at": datetime.now(),
                "password": "hashed_password",
                "salt": "random_salt",
                "address": address,
                "phone": "0724368754",
                "mail": f"user{i}@{domain}"
            }

            customer = Customer(**customer_data)
            assert customer.mail == f"user{i}@{domain}"

    def test_customer_creation_missing_required_fields(self):
        """Test that address, phone and mail are required for Customer"""
        address = Address(
            street_number="789",
            street_name="Pine Road",
            postal_code="13001",
            city="Marseille",
            country="France"
        )

        # Test missing address
        customer_data_no_address = {
            "id": 2,
            "first_name": "Neo",
            "last_name": "Wilson",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "phone": "0612345678",
            "mail": "neo.wilson@gmail.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            Customer(**customer_data_no_address)
        assert "address" in str(exc_info.value)

        # Test missing phone
        customer_data_no_phone = {
            "id": 3,
            "first_name": "Chahid",
            "last_name": "Brown",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "address": address,
            "mail": "chahid.brown@gmail.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            Customer(**customer_data_no_phone)
        assert "phone" in str(exc_info.value)

        # Test missing mail
        customer_data_no_mail = {
            "id": 4,
            "first_name": "Wandrille",
            "last_name": "Donald",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "address": address,
            "phone": "0798765432"
        }

        with pytest.raises(ValidationError) as exc_info:
            Customer(**customer_data_no_mail)
        assert "mail" in str(exc_info.value)

    def test_customer_creation_invalid_phone_type(self):
        """Test that phone must be a string"""
        address = Address(
            street_number="321",
            street_name="Elm Street",
            postal_code="31000",
            city="Toulouse",
            country="France"
        )

        customer_data = {
            "id": 5,
            "first_name": "Emma",
            "last_name": "Davis",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "address": address,
            "phone": 1234567890,
            "mail": "emma.davis@gmail.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            Customer(**customer_data)
        assert "string" in str(exc_info.value).lower()

    def test_customer_creation_email_empty_local_part(self):
        """Test that email with empty local part raises ValidationError"""
        address = Address(
            street_number="654",
            street_name="Maple Lane",
            postal_code="44000",
            city="Nantes",
            country="France"
        )

        invalid_emails = [
            "@gmail.com",           # Local part vide
            " @gmail.com",          # Local part avec espace
            "  @gmail.com",         # Local part avec espaces
        ]

        for invalid_email in invalid_emails:
            customer_data = {
                "id": 6,
                "first_name": "Frank",
                "last_name": "Miller",
                "created_at": datetime.now(),
                "password": "hashed_password",
                "salt": "random_salt",
                "address": address,
                "phone": "0687654321",
                "mail": invalid_email
            }

            with pytest.raises(ValidationError) as exc_info:
                Customer(**customer_data)
            assert "mail" in str(exc_info.value).lower()

    def test_customer_creation_email_special_characters_in_local_part(self):
        """Test that email with special characters in local part raises ValidationError"""
        address = Address(
            street_number="987",
            street_name="Cedar Blvd",
            postal_code="59000",
            city="Lille",
            country="France"
        )

        invalid_emails = [
            "user@name@gmail.com",  # @ in the local part
            "user name@gmail.com",  # space in the local part
            "user+name@gmail.com",  # + in the local part
            "user#name@gmail.com",  # # in the local part
            "user$name@gmail.com",  # $ in the local part
            "user&name@gmail.com",  # & in the local part
            "user!name@gmail.com",  # ! in the local part
        ]

        for invalid_email in invalid_emails:
            customer_data = {
                "id": 7,
                "first_name": "Neo",
                "last_name": "Taylor",
                "created_at": datetime.now(),
                "password": "hashed_password",
                "salt": "random_salt",
                "address": address,
                "phone": "0612345678",
                "mail": invalid_email
            }

            with pytest.raises(ValidationError) as exc_info:
                Customer(**customer_data)
            assert "mail" in str(exc_info.value).lower()

    def test_customer_creation_email_invalid_domain(self):
        """Test that email with invalid domain raises ValidationError"""
        address = Address(
            street_number="147",
            street_name="Birch Street",
            postal_code="67000",
            city="Strasbourg",
            country="France"
        )

        invalid_domains = [
            "user@invalid-domain.com",
            "user@protonmail.com",
            "user@outlook.com", 
            "user@entreprise.fr",
            "user@universite.fr",
        ]

        for invalid_email in invalid_domains:
            customer_data = {
                "id": 8,
                "first_name": "Martin",
                "last_name": "Clark",
                "created_at": datetime.now(),
                "password": "hashed_password",
                "salt": "random_salt",
                "address": address,
                "phone": "0798765432",
                "mail": invalid_email
            }

            with pytest.raises(ValidationError) as exc_info:
                Customer(**customer_data)
            assert "mail" in str(exc_info.value).lower()

    def test_customer_creation_email_missing_at_symbol(self):
        """Test that email without @ symbol raises ValidationError"""
        address = Address(
            street_number="258",
            street_name="Willow Way",
            postal_code="33000",
            city="Bordeaux",
            country="France"
        )

        invalid_emails = [
            "usergmail.com",        # @ missing
            "user.gmail.com",
            "user gmail.com",
        ]

        for invalid_email in invalid_emails:
            customer_data = {
                "id": 9,
                "first_name": "Chahid",
                "last_name": "Anderson",
                "created_at": datetime.now(),
                "password": "hashed_password",
                "salt": "random_salt",
                "address": address,
                "phone": "0724368754",
                "mail": invalid_email
            }

            with pytest.raises(ValidationError) as exc_info:
                Customer(**customer_data)
            assert "mail" in str(exc_info.value).lower()

    def test_customer_creation_phone_empty_string(self):
        """Test that empty string phone raises ValidationError"""
        address = Address(
            street_number="369",
            street_name="Aspen Drive",
            postal_code="06000",
            city="Nice",
            country="France"
        )

        customer_data = {
            "id": 10,
            "first_name": "Emma",
            "last_name": "Roberts",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "address": address,
            "phone": "",
            "mail": "emma.roberts@gmail.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            Customer(**customer_data)
        assert "phone" in str(exc_info.value).lower()

    def test_customer_creation_phone_whitespace_only(self):
        """Test that whitespace-only phone raises ValidationError"""
        address = Address(
            street_number="741",
            street_name="Magnolia Court",
            postal_code="35000",
            city="Rennes",
            country="France"
        )

        customer_data = {
            "id": 11,
            "first_name": "Wandrille",
            "last_name": "Lee",
            "created_at": datetime.now(),
            "password": "hashed_password",
            "salt": "random_salt",
            "address": address,
            "phone": "   ",
            "mail": "wandrille.lee@gmail.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            Customer(**customer_data)
        assert "phone" in str(exc_info.value).lower()

    def test_customer_phone_uniqueness_same_format(self):
        """Test that duplicate phone numbers in same format raise error"""
        address = Address(
            street_number="852",
            street_name="Spruce Street",
            postal_code="37000",
            city="Tours",
            country="France"
        )

        # First customer
        customer1_data = {
            "id": 12,
            "first_name": "Leo",
            "last_name": "Garcia",
            "created_at": datetime.now(),
            "password": "hashed_password1",
            "salt": "salt1",
            "address": address,
            "phone": "0724368754",
            "mail": "leo.garcia@gmail.com"
        }

        customer1 = Customer(**customer1_data)

        # Attempt to create second customer with same phone
        customer2_data = {
            "id": 13,
            "first_name": "Mia",
            "last_name": "Martinez",
            "created_at": datetime.now(),
            "password": "hashed_password2",
            "salt": "salt2",
            "address": address,
            "phone": "0724368754",
            "mail": "mia.martinez@free.fr"
        }

        with pytest.raises(ValueError, match="Phone number already used"):
            self._check_phone_uniqueness(customer2_data, [customer1])

    def test_customer_email_uniqueness(self):
        """Test that duplicate email addresses raise error"""
        address = Address(
            street_number="963",
            street_name="Poplar Avenue",
            postal_code="84000",
            city="Avignon",
            country="France"
        )
        
        # First customer
        customer1_data = {
            "id": 14,
            "first_name": "Noah",
            "last_name": "Lopez",
            "created_at": datetime.now(),
            "password": "hashed_password1",
            "salt": "salt1",
            "address": address,
            "phone": "0612345678",
            "mail": "noah.lopez@orange.fr"
        }

        customer1 = Customer(**customer1_data)

        # Attempt to create second customer with same email
        customer2_data = {
            "id": 15,
            "first_name": "Olivia",
            "last_name": "Harris",
            "created_at": datetime.now(),
            "password": "hashed_password2",
            "salt": "salt2",
            "address": address,
            "phone": "0798765432",
            "mail": "noah.lopez@orange.fr"
        }

        with pytest.raises(ValueError, match="Email address already used"):
            self._check_email_uniqueness(customer2_data, [customer1])

    def test_customer_valid_local_part_characters(self):
        """Test that valid local part characters are accepted"""
        address = Address(
            street_number="159",
            street_name="Sycamore Lane",
            postal_code="45000",
            city="Orléans",
            country="France"
        )
        
        valid_emails = [
            "user123@gmail.com",           # Chiffres
            "user.name@gmail.com",         # Point
            "username@gmail.com",          # Lettres seulement
            "u@gmail.com",                 # Local part court
            "verylonglocalpart@gmail.com", # Local part long
        ]
        
        for i, valid_email in enumerate(valid_emails):
            customer_data = {
                "id": 200 + i,
                "first_name": f"Test{i}",
                "last_name": "Valid",
                "created_at": datetime.now(),
                "password": "hashed_password",
                "salt": "random_salt",
                "address": address,
                "phone": "0724368754",
                "mail": valid_email
            }
            
            customer = Customer(**customer_data)
            assert customer.mail == valid_email

    def _check_phone_uniqueness(self, new_customer_data, existing_customers):
        """Helper method to check phone uniqueness"""
        new_phone = new_customer_data["phone"]
        new_phone_normalized = self._normalize_phone(new_phone)

        for existing_customer in existing_customers:
            existing_phone_normalized = self._normalize_phone(existing_customer.phone)
            if new_phone_normalized == existing_phone_normalized:
                raise ValueError("Phone number already used")

        return True

    def _check_email_uniqueness(self, new_customer_data, existing_customers):
        """Helper method to check email uniqueness"""
        new_email = new_customer_data["mail"].lower().strip()

        for existing_customer in existing_customers:
            existing_email = existing_customer.mail.lower().strip()
            if new_email == existing_email:
                raise ValueError("Email address already used")

        return True

    def _normalize_phone(self, phone):
        """Normalize phone number for comparison"""
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