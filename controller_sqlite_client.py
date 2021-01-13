import sqlite3
import time


class ControllerSqlite:
    def __init__(self, database_name, id_col_name='lightbulb_id', status_col_name='lightbulb_status'):
        self.database_name = database_name
        self.id_col_name = id_col_name
        self.status_col_name = status_col_name
        self.table_name = None
        self.sqlite_connection = None
        self.cursor = None

    def connect_to_database(self):
        try:
            self.sqlite_connection = sqlite3.connect(self.database_name, check_same_thread=False)
            self.cursor = self.sqlite_connection.cursor()
            return f"Baza danych: {self.database_name} zostala stworzona i poprawnie polaczona z SQLite"
        except sqlite3.Error as error:
            return f"Napotkano problem przy probie polaczenia z baza danych: {error}"

    def create_table_if_dosent_exists(self, table_name):
        try:
            self.table_name = table_name
            sqlite_create_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} " \
                                  f"({self.id_col_name} TEXT PRIMARY KEY NOT NULL, " \
                                  f"{self.status_col_name} TEXT " \
                                  f"CHECK ({self.status_col_name} = 'ON' OR {self.status_col_name} = 'OFF' " \
                                  f"OR {self.status_col_name} = '?'))"
            self.cursor.execute(sqlite_create_query)
            self.sqlite_connection.commit()
            return f"Poprawnie stworzono tabele: {table_name}"
        except sqlite3.Error as error:
            return f"Napotkano problem podczas tworzenia tabeli: {error}"

    def add_lightbulb(self, lightbulb_id, lightbulb_status):
        try:
            sqlite_insert_query = f"INSERT INTO {self.table_name} ({self.id_col_name}, {self.status_col_name}) " \
                                  f"VALUES('{lightbulb_id}', '{lightbulb_status}');"
            self.cursor.execute(sqlite_insert_query)

            if self.cursor.lastrowid != 0:  # jesli ostatni wiersz ma rowid == 0 tzn ze nic nie dodano
                self.sqlite_connection.commit()
                return f"Poprawnie dodano wpis o urzdzeniu: {lightbulb_id} do bazy danych"
            else:
                raise sqlite3.Error
        except sqlite3.Error as error:
            return f"Napotkano problem podczas dodawania rekordu do bazy danych: {error}"

    def change_status_lightbulb(self, new_status, record_id):
        try:

            sql_update_query = f"Update {self.table_name} SET {self.status_col_name} = '{new_status}' " \
                               f"where {self.id_col_name} = '{record_id}'"
            self.cursor.execute(sql_update_query)
        except sqlite3.Error as error:
            return "Napotkano problem podczas zmiany statusu urzadzenia: {record_id}, blad: {error}"

    def select_lightbulbs(self, expression):
        try:
            sql_select_query = f"select * from {self.table_name} {expression}"
            self.cursor.execute(sql_select_query)
            return self.cursor.fetchall()

        except sqlite3.Error as error:
            return f"Napotkano problem podczas wykonywania polecenia SELECT: {error}"

    def delete_lightbulb(self, lightbulb_id):
        try:
            sql_delete_query = f"DELETE from {self.table_name} where {self.id_col_name} = '{lightbulb_id}'"
            self.cursor.execute(sql_delete_query)
            return f'Poprwanie usunieto urzadzenie: {lightbulb_id} z bazy danych!'
        except sqlite3.Error as error:
            return f"Napotkano problem podczas usuwania urzadzenia: {lightbulb_id} z bazy danych: {error}"

    def delete_table(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.sqlite_connection.commit()
