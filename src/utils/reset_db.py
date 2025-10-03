from dotenv import load_dotenv

from DAO.DBConnector import DBConnector

from .singleton import Singleton

load_dotenv()


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")
        dbconnector = DBConnector()

        init_db = open("database_scripts/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        # print(init_db_as_string[:7])
        # pop_db = open("database_scripts/pop_db.sql", encoding="utf-8")
        # pop_db_as_string = pop_db.read()

        try:
            dbconnector.sql_query(query=init_db_as_string, return_type="none")
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données - Terminée")

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
