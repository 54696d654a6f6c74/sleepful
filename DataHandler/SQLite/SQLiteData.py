from DataHandler import DataHandler

import sqlite3


class SQLiteData(DataHandler):
    def __init__(self, path: str):
        self.db_path = path

        self.table_name = path.split('/')[-1] if path[-1] != '/' else path.split('/')[-2]

    def __enter__(self) -> object:
        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()

        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self._close()

    def __del__(self):
        self._close()

    def _close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def get_data_field(self, index: int, field_name: str) -> dict:
        query = "SELECT {0} FROM {1} WHERE id = {2}".format(field_name, self.table_name, index)
        self.cursor.execute(query)

        return self.cursor.fetchall()[0]

    def get_data_fields(self, index: int, fields: list, sort_data: bool = False) -> dict:
        field_names = str.join(", ", fields)
        query = "SELECT {0} FROM {1} WHERE id = {2}".format(field_names, self.table_name, index)
        self.cursor.execute(query)

        if sort_data:
            return sorted(self.cursor.fetchall())
        return self.cursor.fetchall()

    def get_all_entry_indices(self, sort_data: bool = True) -> list:
        query = "SELECT id FORM {0}".format(self.table_name)
        self.cursor.execute(query)

        if sort_data:
            return sorted(self.cursor.fetchall())
        return self.cursor.fetchall()

    def update_data(self, index: int, field_name: str, payload: str):
        query = "UPDATE {0} SET {1} = {2} WHERE id = {3}".format(self.table_name, field_name, payload, index)
        self.cursor.execute(query)

    def update_multiple(self, index: int, fields: list, payload: dict):
        assignments = ["{0} = {1}".format(x, payload[x]) for x in fields]
        assignments = str.join(", ", assignments)
        query = "UPDATE {0} SET {1} WHERE id = {2}".format(self.table_name, assignments, index)
        self.cursor.execute(query)

    def new_data(self, payload: dict):
        fields = str.join(", ", payload.keys())
        values = str.join(", ", payload.values())
        query = "INSERT INTO {0} ({1}) VALUES ({2})".format(self.table_name, fields, values)
        self.cursor.execute(query)

    def remove_data(self, index: int):
        query = "DELETE FROM {0} WHERE id = {1}".format(self.table_name, index)
        self.cursor.execute(query)
