from abc import ABC, abstractmethod


class DataHandler(ABC):
    @abstractmethod
    def __init__(self, root_path: str):
        ...

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exec_type, exec_value, traceback):
        ...

    @abstractmethod
    def get_data_field(self, index: int, field_name: str) -> dict:
        ...

    def get_data_fields(self, index: int, fields: list, sort_data: bool = False) -> dict:
        ...

    def get_all_entry_indices(self, sort_data: bool = True) -> list:
        ...

    @abstractmethod
    def update_data(self, index: int, field_name: str, payload: str):
        ...

    @abstractmethod
    def update_multiple(self, index: int, fields: list, payload: str):
        ...

    @abstractmethod
    def new_data(self, payload: dict):
        ...

    @abstractmethod
    def remove_data(self, index: int):
        ...
