from datetime import datetime

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, password: str, first_name: str, last_name: str) -> User:
        """
        Create a new user with a unique salt and hashed password.

        Parameters
        ----------
        password : str
            Plain text password (before hash)
        first_name : str
            User's first name
        last_name : str
            User's last name

        Returns
        -------
        User
            The created user
        """
        check_password_strength(password)

        salt = create_salt()

        hashed_password = hash_password(password, salt)

        new_user = User(first_name, last_name, hashed_password, salt, created_at=datetime.now())

        new_user = self.user_repo.insert_into_db(
            salt=salt,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )

        return new_user

    def get_user(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)
