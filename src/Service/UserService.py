from typing import Literal, Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def get_user(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def delete_user(self, user_id: int) -> User | None:
        print(f"[UserService] Deleting user with ID: {user_id}")
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError(f"[UserService] Cannot delete: user with ID {user_id} not found.")
        user = self.user_repo.delete_user(user_id)

        print(f"[UserService] User with ID {user_id} has been deleted.")

    def update_user(self, user_id: int, update) -> User | None:
        update_message_parts = []
        for field, value in update.user():
            update_message_parts.append(f"{field}={value}")

        print(f"[UserService] Updating user: {', '.join(update_message_parts)}")

        updated_user = self.user_repo.update_user(user_id=id, update=update)
        print(f"[UserService] Repo returned after creation: {updated_user}")
        return updated_user

    def change_password(self, id_user: int, password: str, new_password: str):
        pass

    def create_user(
        self,
        password: str,
        username: str,
        email: str,
        role: Literal["admin", "driver", "customer"],
    ):
        try:
            # check_password_strength(password)
            newsalt = create_salt()
            password_hash = hash_password(newsalt, password)
            usrdict = {
                "id": 0,
                "username": username,
                "password_hash": password_hash,
                "salt": newsalt,
                "role": role,
            }
            new_user = User(usrdict)
            self.user_repo.insert_into_db(new_user)
            print("new user sucessfully created")
        except Exception:
            print("user creation error")

    def login(self, username, passwordattempt) -> User:
        try:
            val = validate_password(username, passwordattempt, self.user_repo)
            if val:
                return self.user_repo.get_by_username(username)
            else:
                print("pw validation error")
                
    def logout(self):
        pass
