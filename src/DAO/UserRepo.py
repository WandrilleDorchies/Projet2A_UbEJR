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

    def insert_into_db(self, user: User) -> User:
        raw_created_user = self.db_connector.sql_query(
            """
        INSERT INTO users (id, first_name, last_name, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """,
            {"username": username, "salt": salt, "password": hashed_password},
            "one",
        )
        # pyrefly: ignore
        return User(**raw_created_user)

    def update_user(self, user_id, first_name, last_name, hashed_password, type) -> User:
        raw_update_user = self.db_connector.sql_query(
            """
        UPDATE User SET first_name = %(first_name)s, last_name=%(last_name)s,
        hashed_password=%(hashed_password)s, type=%(type)s
        WHERE user_id=%(user_id)s RETURNING *;
        """,
            {"key": 1},
            "one",
        )
        return User(**raw_update_user)

    def delete_user(self, user_id) -> User:
        raw_delete_user = self.db_connector.sql_query(
            """
        DELETE FROM User WHERE user_id=%s
        """,
            "one",
        )
        return User(**raw_delete_user)
