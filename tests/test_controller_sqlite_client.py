import unittest
from controller_sqlite_client import ControllerSqlite

class TestControllerSqlite(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestControllerSqlite, self).__init__(*args, **kwargs)
        self.sql_test = ControllerSqlite(database_name="test_sql.sqlite3", id_col_name='test_id',
                                         status_col_name='test_status')

    def test_connect_to_database(self):
        self.sql_test.connect_to_database()
        assert self.sql_test.cursor.connection == self.sql_test.sqlite_connection

    def test_create_table_if_dosent_exists(self):
        self.sql_test.connect_to_database()
        self.sql_test.create_table_if_dosent_exists('test_sql')
        self.sql_test.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_sql';")
        output = self.sql_test.cursor.fetchall()
        assert output[0][0] == 'test_sql'


    def test_add_lightbulb(self):
        self.sql_test.connect_to_database()
        self.sql_test.create_table_if_dosent_exists('test_sql') # tutaj dekalrowana jest nazwa tabeli
        self.sql_test.add_lightbulb('TEST','ON')
        output = self.sql_test.select_lightbulbs(expression="")
        assert output[0][0] == 'TEST' and output[0][1] == 'ON'
        # zawsze doda tylko jedna, wiec mozna na stale ustalic ktory rekord sprawdza

    def test_change_status_of_lightbulb(self):
        self.sql_test.connect_to_database()
        self.sql_test.create_table_if_dosent_exists('test_sql')
        self.sql_test.add_lightbulb('TEST','ON')
        self.sql_test.change_status_lightbulb('OFF', 'TEST')
        output = self.sql_test.select_lightbulbs(expression="")
        assert output[0][0] == 'TEST' and output[0][1] == 'OFF'
    
    def test_select_lightbulbs(self):
        self.sql_test.connect_to_database()
        self.sql_test.create_table_if_dosent_exists('test_sql')
        self.sql_test.add_lightbulb('TEST','ON')
        self.sql_test.change_status_lightbulb('OFF', 'TEST')
        output = self.sql_test.select_lightbulbs(expression="")
        assert output[0][0] == 'TEST' and output[0][1] == 'OFF'

    def test_delete_lightbulbs(self):
        self.sql_test.connect_to_database()
        self.sql_test.create_table_if_dosent_exists('test_sql')
        self.sql_test.add_lightbulb('TEST','ON')
        self.sql_test.change_status_lightbulb('OFF', 'TEST')
        self.sql_test.delete_lightbulb('TEST')
        self.sql_test.select_lightbulbs(expression="")
        output = self.sql_test.cursor.fetchall()
        assert output == []

    def test_delete_table(self):
        self.sql_test.connect_to_database()
        self.sql_test.create_table_if_dosent_exists('test_sql')
        self.sql_test.delete_table()
        self.sql_test.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_sql';")
        output = self.sql_test.cursor.fetchall()
        assert output == []

if __name__ == '__main__':
    unittest.main()