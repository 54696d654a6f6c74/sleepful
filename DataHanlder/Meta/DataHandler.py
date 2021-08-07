from abc import ABC, abstractclassmethod


class DataHandler(ABC):
    @abstractclassmethod
    def __init__(self, root_path: str):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exce_type, exec_value, traceback):
        ...

    @abstractclassmethod
    def get_data_field(self, field_name: str):
        ...

    def get_data_fields(self, container_handle: str, sort_data: bool = True) -> [dict]:
        ...

    @abstractclassmethod
    def update_data(self, data_type: str, index: int, field_name: str, payload: str):
        ...

    @abstractclassmethod
    def update_all_data(self, data_type: str, index: int, payload: str):
        ...

    @abstractclassmethod
    def new_data(self, data_type: str, payload: str):
        ...

    @abstractclassmethod
    def remove_data(self, data_type: str, index: int):
        ...
