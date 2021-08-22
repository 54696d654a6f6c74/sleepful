from abc import ABC, abstractmethod
from flask import Blueprint
from typing import Callable

from DataHanlder import DataHandler


class Behavior(ABC):
    @abstractmethod
    def __init__(self, route: str, data_handler: type[DataHandler], **args):
        ...

    @abstractmethod
    def _bind(self, bp: Blueprint):
        ...

    def bind(self, bp: Blueprint, auth: Callable = None, **auth_opts):
        if auth is not None:
            bp.before_request(lambda: auth(**auth_opts))
            pass

        self._bind(bp)
