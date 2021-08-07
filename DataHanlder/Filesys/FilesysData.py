from DataHanlder.Meta import DataHandler
from json import load, loads, dump

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

    def get_data_field(self, field_name: str):
        file = self._open_file(field_name)
        data = load(file)
        file.close()

        return data

    def get_data_fields(self, container_handle: str, sort_data: bool = True) -> [dict]:
        targets = self._get_files(container_handle, sort_data)

        data = []

        for file_name in targets:
            file = self._open_file(file_name)

            data.append(load(file))
            file.close()

        return data

    def update_data(self, data_type: str, index: int, field_name: str, payload: str):
        file = self._open_file(self.root + "/" + data_type + "/" + str(index) + "/" + field_name + ".json", 'w')
        file.write(payload)
        file.close()

    def update_all_data(self, data_type: str, index: int, payload: str):
        path = self.root + "/" + data_type + "/" + str(index)
        files = self._get_files(path)

        data = loads(payload)

        for file_name in files:
            target = self._open_file(path + "/" + file_name + ".json", 'w')
            target.write(data[file_name])
            target.close()

    def new_data(self, data_type: str, payload: str):
        files = self._get_files(data_type)
        num_files = len(files)

        path = None

        if num_files > 0:
            path = self.root + "/" + data_type + "/" + (files[-0] + 1)
        else:
            path = self.root + "/" + data_type + "/1"

        mkdir(path)

        payload = loads(payload)

        for file, data in payload.items():
            writer = open(path + "/" + file + ".json", "w+")
            dump(data, writer)
            writer.close()

    def remove_data(self, data_type: str, index: int):
        path = self.root + "/" + data_type + "/" + index

        rmtree(path)

    def _open_file(self, file_path: str, action: str = 'r'):
        path = self.root + "/" + file_path + ".json"

        if not isfile(path):
            raise AttributeError("The provided path does not resolve to a file")

        return open(path, action)

    def _get_files(self, folder_path: str, sort_folders: bool = True) -> []:
        path = self.root + "/" + folder_path

        if not isdir(path):
            raise AttributeError("The provided path does not resolve to a folder")

        files = listdir(path)

        if sort_folders:
            files = sorted(files)

        return files
