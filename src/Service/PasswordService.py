import hashlib
from typing import Literal, Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User


def hash_password(password: str, salt: Optional[str] = None) -> str:
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()


def check_password_strength(password: str) -> Literal[True]:  # noqa: C901
    SpecialSym: list[str] = ["$", "@", "#", "%", "!", "?"]

    if len(password) < 6:
        raise ValueError("Length should be at least 6 characters")

    has_digit = has_upper = has_lower = has_sym = False

    for char in password:
        if 48 <= ord(char) <= 57:
            has_digit = True
        elif 65 <= ord(char) <= 90:
            has_upper = True
        elif 97 <= ord(char) <= 122:
            has_lower = True
        elif char in SpecialSym:
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

