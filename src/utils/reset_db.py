from src.DAO.DBConnector import DBConnector

from .singleton import Singleton


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")

        init_db = open("database_scripts/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        print(init_db_as_string[:7])
        # pop_db = open("database_scripts/pop_db.sql", encoding="utf-8")
        # pop_db_as_string = pop_db.read()

        try:
            DBConnector.sql_query(query=init_db_as_string)
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données - Terminée")

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
