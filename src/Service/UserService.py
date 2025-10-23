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

        print(f"[UserService] Updating user: {", ".join(update_message_parts)}")

        updated_user = self.user_repo.update_user(user_id=id, update=update)
        print(f"[UserService] Repo returned after creation: {updated_user}")
        return updated_user

    def change_password(self, id_user:int, password:str, new_password:str) :
        pass 

    def create_user(self, user_id:int, password:str, type) : 
        pass
    
    def login(self, username, password) : 
        pass

    def logout(self):
        pass 
    
    def create_user():
        pass
        #user = self.user_repo.insert_into_db()

