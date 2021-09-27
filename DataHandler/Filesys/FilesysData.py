from DataHandler import DataHandler
from json import load, dump, dumps

from os.path import isdir, isfile
from os import listdir, mkdir
from shutil import rmtree


class FilesysData(DataHandler):
    def __init__(self, root_path: str):
        self.root = root_path

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        pass

    def get_data_field(self, index: int, field_name: str) -> dict:
        file = self._open_file(f"{str(index)}/{field_name}")
        data = load(file)
        file.close()

        return data

    def get_data_fields(self, index: int, fields: list, sort_data: bool = False) -> dict:
        data = {}

        for file_name in fields:
            file = self._open_file(f"{str(index)}/{file_name}")
            data[file_name] = load(file)
            file.close()

        return data

    def get_all_entry_indices(self, sort_data: bool = True) -> list:
        all_entries = self._get_files(sort_data = sort_data)

        return all_entries

    def update_data(self, index: int, field_name: str, payload: str):
        file = self._open_file(f"{str(index)}/{field_name}", 'w')
        file.write(payload)
        file.close()

    def update_multiple(self, index: int, fields: list, payload: str):
        path = str(index)

        for file_name in fields:
            target = self._open_file(f"{path}/{file_name}", 'w')
            target.write(dumps(payload[file_name]))
            target.close()

    def new_data(self, payload: dict):
        files = self._get_files()
        num_files = len(files)

        path = None

        if num_files > 0:
            path = f"{self.root}/{str(int(files[-1]) + 1)}"
        else:
            path = f"{self.root}/1"

        mkdir(path)

        for file, data in payload.items():
            writer = open(f"{path}/{file}.json", "w+")
            dump(data, writer)
            writer.close()

    def remove_data(self, index: int):
        path = f"{self.root}/{index}"

        rmtree(path)

    def _open_file(self, file_path: str, action: str = 'r'):
        path = f"{self.root}/{file_path}.json"

        if not isfile(path):
            raise AttributeError("The provided path does not resolve to a file")

        return open(path, action)

    def _get_files(self, folder_path: str = "", sort_data: bool = True) -> list:
        path = f"{self.root}/{folder_path}"

        if not isdir(path):
            raise AttributeError("The provided path does not resolve to a folder")

        files = listdir(path)

        if sort_data:
            files = sorted(files)

        return files
