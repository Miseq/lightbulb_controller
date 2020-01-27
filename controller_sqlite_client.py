import sqlite3

class ControllerSqlite:
    def __init__(self, database_name, id_col_name='lightbulb_id', status_col_name='lightbulb_status'):
        self.database_name = database_name
        # Zainicjowane pozniej w odpowiednich metodach
        self.id_col_name = id_col_name
        self.status_col_name = status_col_name
        self.table_name = None
        self.sqlite_connection = None
        self.cursor = None

    def connect_to_database(self):
        try:
            self.sqlite_connection = sqlite3.connect(self.database_name, check_same_thread=False)
            self.cursor = self.sqlite_connection.cursor()
            print("Database created and Successfully Connected to SQLite")
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_table_if_dosent_exists(self, table_name):
        try:
            self.table_name = table_name
            sqlite_create_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} " \
                                  f"({self.id_col_name} TEXT PRIMARY KEY NOT NULL, " \
                                  f"{self.status_col_name} TEXT " \
                                  f"CHECK ({self.status_col_name} = 'ON' OR {self.status_col_name} = 'OFF' " \
                                  f"OR {self.status_col_name} = '?'))"
            self.cursor.execute(sqlite_create_query)
            print(f"Succesfully created table {table_name}")
        except sqlite3.Error as error:
            print("Error while creating table: ", error)

    def add_lightbulb(self, lightbulb_id, lightbulb_status):
        try:
            sqlite_insert_query = f"INSERT INTO {self.table_name} ({self.id_col_name}, {self.status_col_name}) " \
                                  f"VALUES('{lightbulb_id}', '{lightbulb_status}');"
            self.cursor.execute(sqlite_insert_query)

            if self.cursor.lastrowid != 0: # jesli ostatni wiersz ma rowid == 0 tzn ze nic nie dodano
                self.sqlite_connection.commit()
                print(f"Succesfully added record of lightbulb {lightbulb_id} to database")
            else:
                raise sqlite3.Error
        except sqlite3.Error as error:
            print(f"Error while adding record to database: {error}")

    def change_status_lightbulb(self, new_status, record_id):
        try:

            sql_update_query = f"Update {self.table_name} SET {self.status_col_name} = '{new_status}' " \
                               f"where {self.id_col_name} = '{record_id}'"
            self.cursor.execute(sql_update_query)
        except sqlite3.Error as error:
            print(f"Error while changing status of: {record_id}, error:", error)


    def select_lightbulbs(self, expression):
        try:
            sql_select_query = f"select * from {self.table_name} {expression}"
            self.cursor.execute(sql_select_query)
            return(self.cursor.fetchall())

        except sqlite3.Error as error:
            print("Error while selecting recods from database", error)

    def delete_lightbulb(self, lightbulb_id):
        try:
            sql_delete_query = f"DELETE from {self.table_name} where {self.id_col_name} = '{lightbulb_id}'"
            self.cursor.execute(sql_delete_query)
            #TODO sprawdzic czy trzeba dawac ten commit
            print(f'Succesfully removed lightbulb {lightbulb_id} from database!')
        except sqlite3.Error as error:
            print(f"Error while deleting {lightbulb_id} from database: {error}")

    def delete_table(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.sqlite_connection.commit()



#TODO jak bd czas to dodac topic - still active w ktorym po kazdej otrzymanej komendzie odsyla publikacje swojego id zeby kontroler wiedzial ze to jest dalej aktywne
