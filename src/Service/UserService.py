from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, hash_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, username: str, password: str) -> User:
        if not check_password_strength(password):
            return False

        hash_pw = hash_password(password, username)

        self.user_repo.insert_into_db(username, hash_pw)

        return

    def get_user(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)
