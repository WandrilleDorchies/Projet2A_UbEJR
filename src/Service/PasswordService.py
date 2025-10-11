import hashlib
import secrets
from typing import TYPE_CHECKING, Literal, Optional

from src.DAO.UserRepo import UserRepo

if TYPE_CHECKING:
    from src.Model.User import User


def create_salt() -> str:
    """
    Generate a salt

    Return
    ------
        str: A string of 256 character
    """
    return secrets.token_hex(128)


def hash_password(password: str, salt: str) -> str:
    """
    Hash a password with SHA-256

    Parameters
    ----------
    password: str
        The password of an user

    salt: str
        Additionnal string unique for each user

    Return
    ------
        str: The hashed password and salt
    """
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()


def check_password_strength(password: str) -> Literal[True]:  # noqa: C901
    """
    Validate that a password meets security requirements.

    Requirements:
    - At least 6 characters long
    - At least one digit (0-9)
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one special character ($@#%!?)

    Parameters
    ----------
    password : str
        Password to validate

    Returns
    -------
    bool:
        True if password meets all requirements, else raise a ValueError
    """
    symbols: list[str] = ["$", "@", "#", "%", "!", "?"]

    if len(password) < 6:
        raise ValueError("Length should be at least 6 characters")

    has_digit = has_upper = has_lower = has_sym = False

    for char in password:
        if char.isdigit():
            has_digit = True
        elif char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char in symbols:
            has_sym = True

    if not has_digit:
        raise ValueError("Password should have at least one numeral")

    if not has_upper:
        raise ValueError("Password should have at least one uppercase letter")

    if not has_lower:
        raise ValueError("Password should have at least one lowercase letter")

    if not has_sym:
        raise ValueError("Password should have at least one of the symbols $@#%?!")

    return True


def validate_password(user_id: int, password: str) -> bool:
    """
    Validate username and password combination

    Parameters
    ----------
    user_id : int
        Id of the user
    password : str
        Password to check

    Returns
    -------
    bool
        True if the password is correct, else raise en Error
    """
    user: Optional[User] = UserRepo().get_by_id(user_id)

    if user is None:
        raise ValueError(f"User {user_id} not found")

    test_password: str = hash_password(password, user.salt)

    if user.password != test_password:
        raise ValueError("Incorrect password")

    return True
