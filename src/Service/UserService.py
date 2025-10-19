from datetime import datetime

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_hashed_password(self, password: str) -> str:
        """
        Create a new user with a unique salt and hashed password.

        Parameters
        ----------
        password : str
            Plain text password (before hash)

        Returns
        -------
        str
            The hashed password
        """
        check_password_strength(password)

        salt = create_salt()

        hashed_password = hash_password(password, salt)

        return hashed_password

    def get_user(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def delete_user(self, user_id: int) -> User | None:
        pass

    def update_user(self, user: User) -> User | None:
        pass
