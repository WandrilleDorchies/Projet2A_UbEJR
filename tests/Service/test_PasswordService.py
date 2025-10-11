# tests/Service/test_PasswordService.py
from datetime import datetime

import pytest

from src.Model.User import User
from src.Service.PasswordService import (
    check_password_strength,
    create_salt,
    hash_password,
    validate_username_password,
)


def test_hash_password_with_salt():
    """Test hashing with salt"""
    password = "mypassword"
    salt = "mysalt"
    hashed = hash_password(password, salt)

    assert hashed == "9109595ebca0d656f8166d6c2a5ec2bb851d4607c323d735e50b83ebc5e0a1e6"


def test_hash_password_different_salts_different_hashes():
    """Test that different salts produce different hashes"""
    password = "mypassword"
    salt1 = "salt1"
    salt2 = "salt2"

    hash1 = hash_password(password, salt1)
    hash2 = hash_password(password, salt2)

    assert hash1 != hash2


def test_hash_password_same_inputs_same_output():
    """Test deterministic behavior"""
    password = "test123"
    salt = "testsalt"

    hash1 = hash_password(password, salt)
    hash2 = hash_password(password, salt)

    assert hash1 == hash2


def test_hash_password_empty_password():
    """Test hashing empty password"""
    hashed = hash_password("", "salt")

    assert hashed is not None
    assert len(hashed) == 64


def test_hash_password_none_salt():
    """Test hashing with None as salt"""
    password = "mypassword"
    hashed = hash_password(password, None)

    assert hashed is not None
    assert len(hashed) == 64


# ============================================================================
# Tests pour create_salt
# ============================================================================


def test_create_salt_returns_string():
    """Test that create_salt returns a string"""
    salt = create_salt()

    assert isinstance(salt, str)


def test_create_salt_correct_length():
    """Test that salt has correct length (256 characters)"""
    salt = create_salt()

    assert len(salt) == 256


def test_create_salt_is_hexadecimal():
    """Test that salt contains only hex characters"""
    salt = create_salt()

    try:
        int(salt, 16)
        is_hex = True
    except ValueError:
        is_hex = False

    assert is_hex


def test_create_salt_is_unique():
    """Test that multiple calls produce different salts"""
    salt1 = create_salt()
    salt2 = create_salt()
    salt3 = create_salt()

    assert salt1 != salt2
    assert salt2 != salt3
    assert salt1 != salt3


def test_create_salt_generates_100_unique_salts():
    """Test generating many salts to ensure randomness"""
    salts = [create_salt() for _ in range(100)]

    # All salts should be unique
    assert len(set(salts)) == 100


# ============================================================================
# Tests pour check_password_strength
# ============================================================================


def test_check_password_strength_valid_password():
    """Test valid passwords"""
    assert check_password_strength("Valid1@") is True
    assert check_password_strength("MyP@ss123") is True
    assert check_password_strength("Str0ng!Pass") is True


def test_check_password_strength_empty():
    """Test empty password"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        check_password_strength("")


def test_check_password_strength_too_short():
    """Test password shorter than 6 characters"""
    with pytest.raises(ValueError, match="Length should be at least 6 characters"):
        check_password_strength("Ab1@")


def test_check_password_strength_exactly_6_chars():
    """Test password with exactly 6 characters (minimum valid)"""
    assert check_password_strength("Aa1@bc") is True


def test_check_password_strength_no_digit():
    """Test password without digit"""
    with pytest.raises(ValueError, match="Password should have at least one numeral"):
        check_password_strength("Abcdef@")


def test_check_password_strength_no_uppercase():
    """Test password without uppercase letter"""
    with pytest.raises(ValueError, match="Password should have at least one uppercase letter"):
        check_password_strength("abcd123@")


def test_check_password_strength_no_lowercase():
    """Test password without lowercase letter"""
    with pytest.raises(ValueError, match="Password should have at least one lowercase letter"):
        check_password_strength("ABCD123@")


def test_check_password_strength_no_special_char():
    """Test password without special character"""
    with pytest.raises(ValueError, match="Password should have at least one of the symbols"):
        check_password_strength("Abcd1234")


def test_check_password_strength_all_special_chars_dollar():
    """Test password with $ special character"""
    assert check_password_strength("Valid1$") is True


def test_check_password_strength_all_special_chars_at():
    """Test password with @ special character"""
    assert check_password_strength("Valid1@") is True


def test_check_password_strength_all_special_chars_hash():
    """Test password with # special character"""
    assert check_password_strength("Valid1#") is True


def test_check_password_strength_all_special_chars_percent():
    """Test password with % special character"""
    assert check_password_strength("Valid1%") is True


def test_check_password_strength_all_special_chars_exclamation():
    """Test password with ! special character"""
    assert check_password_strength("Valid1!") is True


def test_check_password_strength_all_special_chars_question():
    """Test password with ? special character"""
    assert check_password_strength("Valid1?") is True


def test_check_password_strength_multiple_special_chars():
    """Test password with multiple special characters"""
    assert check_password_strength("V@lid1#") is True


def test_check_password_strength_invalid_special_char_ampersand():
    """Test that & is not accepted as special char"""
    with pytest.raises(ValueError, match="Password should have at least one of the symbols"):
        check_password_strength("Valid1&")


def test_check_password_strength_invalid_special_char_asterisk():
    """Test that * is not accepted as special char"""
    with pytest.raises(ValueError, match="Password should have at least one of the symbols"):
        check_password_strength("Valid1*")


def test_check_password_strength_with_spaces():
    """Test password with spaces (should fail - spaces not in special chars)"""
    with pytest.raises(ValueError, match="Password should have at least one of the symbols"):
        check_password_strength("Ab 123c")


def test_check_password_strength_long_password():
    """Test very long valid password"""
    long_password = "ThisIsAVeryLongPassword123!WithManyCharacters"
    assert check_password_strength(long_password) is True


def test_check_password_strength_all_requirements_minimal():
    """Test password with minimal requirements (one of each)"""
    assert check_password_strength("Aa1@bc") is True


def test_check_password_strength_multiple_digits():
    """Test password with multiple digits"""
    assert check_password_strength("Pass123@") is True


def test_check_password_strength_multiple_uppercase():
    """Test password with multiple uppercase letters"""
    assert check_password_strength("ABCdef1@") is True


def test_check_password_strength_multiple_lowercase():
    """Test password with multiple lowercase letters"""
    assert check_password_strength("Abcdef1@") is True


# ============================================================================
# Tests pour validate_username_password
# ============================================================================


class MockUserRepo:
    """Mock repository for testing"""

    def get_by_username(self, username: str):
        if username == "validuser":
            return User(
                id=1,
                username="validuser",
                first_name="John",
                last_name="Doe",
                created_at=datetime.now(),
                salt="testsalt",
                password=hash_password("Password123!", "testsalt"),
            )
        elif username == "anotheruser":
            return User(
                id=2,
                username="anotheruser",
                first_name="Jane",
                last_name="Smith",
                created_at=datetime.now(),
                salt="anothersalt",
                password=hash_password("MySecure@99", "anothersalt"),
            )
        return None


def test_validate_username_password_success():
    """Test successful authentication"""
    repo = MockUserRepo()

    user = validate_username_password("validuser", "Password123!", repo)

    assert user is not None
    assert user.username == "validuser"
    assert user.id == 1


def test_validate_username_password_another_user_success():
    """Test successful authentication with another user"""
    repo = MockUserRepo()

    user = validate_username_password("anotheruser", "MySecure@99", repo)

    assert user is not None
    assert user.username == "anotheruser"
    assert user.id == 2


def test_validate_username_password_user_not_found():
    """Test authentication with unknown username"""
    repo = MockUserRepo()

    with pytest.raises(ValueError, match="user with username invaliduser not found"):
        validate_username_password("invaliduser", "Password123!", repo)


def test_validate_username_password_incorrect_password():
    """Test authentication with wrong password"""
    repo = MockUserRepo()

    with pytest.raises(ValueError, match="Incorrect password"):
        validate_username_password("validuser", "WrongPassword!", repo)


def test_validate_username_password_case_sensitive_password():
    """Test that password is case sensitive"""
    repo = MockUserRepo()

    with pytest.raises(ValueError, match="Incorrect password"):
        validate_username_password("validuser", "password123!", repo)


def test_validate_username_password_similar_password():
    """Test with very similar but incorrect password"""
    repo = MockUserRepo()

    with pytest.raises(ValueError, match="Incorrect password"):
        validate_username_password("validuser", "Password123")  # Missing !


def test_validate_username_password_empty_username():
    """Test with empty username"""
    repo = MockUserRepo()

    with pytest.raises(ValueError, match="user with username  not found"):
        validate_username_password("", "Password123!", repo)


def test_validate_username_password_empty_password():
    """Test with empty password"""
    repo = MockUserRepo()

    with pytest.raises(ValueError, match="Incorrect password"):
        validate_username_password("validuser", "", repo)


def test_validate_username_password_returns_correct_user_data():
    """Test that returned user has correct data"""
    repo = MockUserRepo()

    user = validate_username_password("validuser", "Password123!", repo)

    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.salt == "testsalt"


# ============================================================================
# Tests d'intégration
# ============================================================================


def test_full_password_flow_create_and_validate():
    """Test complete flow: create salt, hash password, validate"""
    # Simulate user creation
    password = "MySecure1@"
    salt = create_salt()
    hashed_password = hash_password(password, salt)

    # Verify password strength
    assert check_password_strength(password) is True

    # Verify hashing is deterministic
    assert hash_password(password, salt) == hashed_password

    # Verify wrong password doesn't match
    wrong_hash = hash_password("WrongPass1!", salt)
    assert wrong_hash != hashed_password


def test_two_users_same_password_different_hashes():
    """Test that same password with different salts produces different hashes"""
    password = "SamePassword1@"

    # User 1
    salt1 = create_salt()
    hash1 = hash_password(password, salt1)

    # User 2
    salt2 = create_salt()
    hash2 = hash_password(password, salt2)

    # Salts must be different
    assert salt1 != salt2

    # Hashes must be different even with same password
    assert hash1 != hash2


def test_password_validation_workflow():
    """Test the full validation workflow"""
    # Create user password
    original_password = "TestPass1@"
    salt = create_salt()
    stored_hash = hash_password(original_password, salt)

    # Simulate login: hash input password with stored salt
    input_password = "TestPass1@"
    input_hash = hash_password(input_password, salt)

    # Passwords should match
    assert input_hash == stored_hash

    # Wrong password should not match
    wrong_password = "WrongPass1@"
    wrong_hash = hash_password(wrong_password, salt)
    assert wrong_hash != stored_hash


def test_salt_uniqueness_across_multiple_users():
    """Test that 10 users get 10 different salts"""
    salts = [create_salt() for _ in range(10)]

    # All salts should be unique
    assert len(set(salts)) == 10


def test_password_strength_before_hashing():
    """Test that weak passwords are rejected before hashing"""
    weak_passwords = [
        "short",  # Too short
        "nouppercase1@",  # No uppercase
        "NOLOWERCASE1@",  # No lowercase
        "NoDigits@",  # No digit
        "NoSpecial123",  # No special char
    ]

    for weak_password in weak_passwords:
        with pytest.raises(ValueError):
            check_password_strength(weak_password)


def test_strong_passwords_accepted():
    """Test that various strong passwords are accepted"""
    strong_passwords = [
        "MyPass123!",
        "Secure@Password1",
        "C0mpl3x#Pass",
        "Str0ng$Passw0rd",
        "T3st!ng?Pass",
    ]

    for strong_password in strong_passwords:
        assert check_password_strength(strong_password) is True

        # Also test they can be hashed
        salt = create_salt()
        hashed = hash_password(strong_password, salt)
        assert len(hashed) == 64
