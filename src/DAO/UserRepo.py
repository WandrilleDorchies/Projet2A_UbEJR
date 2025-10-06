from typing import Optional

from src.Model.User import User

from .DBConnector import DBConnector


class UserRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_by_id(self, user_id: int) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from users WHERE id=%s", [user_id], "one")
        if raw_user is None:
            return None
        # pyrefly: ignore
        return User(**raw_user)

    def get_by_username(self, username: str) -> Optional[User]:
        raw_user = self.db_connector.sql_query(
            "SELECT * from users WHERE username=%s", [username], "one"
        )
        if raw_user is None:
            return None
        # pyrefly: ignore
        return User(**raw_user)

    def insert_into_db(self, username: str, salt: str, hashed_password: str) -> User:
        raw_created_user = self.db_connector.sql_query(
            """
        INSERT INTO users (id, username, salt, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """,
            {"username": username, "salt": salt, "password": hashed_password},
            "one",
        )
        # pyrefly: ignore
        return User(**raw_created_user)
