from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector

from .singleton import Singleton

load_dotenv()

# TODO: handle resetting either prod or test, or both
# TODO: option to opopulate database with sample


class ResetDatabase(metaclass=Singleton):
    """
    Resetting the DB
    """

    def startreset(self):
        print("Initiating DB reset...")
        dbconnector = DBConnector()

        init_db = open("database_scripts/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        print("DB reset - Database structure created ")
        # print(init_db_as_string[:7])
        # pop_db = open("database_scripts/pop_db.sql", encoding="utf-8")
        # pop_db_as_string = pop_db.read()

        try:
            dbconnector.sql_query(query=init_db_as_string, return_type="none")
        except Exception as e:
            print(e)
            raise

        print("DB reset completed")
        # TODO : confirm return type
        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
