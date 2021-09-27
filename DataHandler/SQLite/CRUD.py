from DataHandler import DataHandler

import sqlite3


class SQLiteData(DataHandler):
    def __init__(self, path: str):
        self.db_path = path

    def __enter__(self) -> object:
        self.db = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.db.close()

    def __del__(self):
        self.db.close()

    def get_field(self, name: str):
        pass
