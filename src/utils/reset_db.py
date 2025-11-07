import sys

from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector

from .Populate.Faker import fake
from .Populate.Usurper import Usurper
from .singleton import Singleton

load_dotenv()


class ResetDatabase(metaclass=Singleton):
    """
    Resetting the DB
    """

    def startreset(self, schema=("project, test")):
        if "project" in schema:
            self.reset_project()
        if "test" in schema:
            self.reset_test()

        print("DB reset completed")
        return True

    def reset_project(self):
        print("Initiating project DB reset...")
        dbconnector = DBConnector()

        init_db = open("database_scripts/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        try:
            dbconnector.sql_query(query=init_db_as_string, return_type="none")
            usurper = Usurper(fake, dbconnector)
            usurper.populate_database()
        except Exception as e:
            print(e)
            raise
        # TODO : confirm return type
        return True

    def reset_test(self):
        print("Initiating test DB reset...")
        dbconnector = DBConnector(test=True)

        init_db = open("database_scripts/init_db_test.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        print("Tests DB reset - Database structure created ")
        # print(init_db_as_string[:7])
        # pop_db = open("database_scripts/pop_db.sql", encoding="utf-8")
        # pop_db_as_string = pop_db.read()

        try:
            dbconnector.sql_query(query=init_db_as_string, return_type="none")
        except Exception as e:
            print(e)
            raise
        # TODO : confirm return type
        return True


if __name__ == "__main__":
    if len(sys.argv[1:]) > 2:
        print("Too many arguments, only project and test schemas can be reset.")
        sys.exit(1)
    if len(sys.argv) == 1:
        ResetDatabase().startreset()
    else:
        ResetDatabase().startreset(schema=sys.argv[1:])
