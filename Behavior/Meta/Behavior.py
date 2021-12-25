from abc import ABC, abstractmethod
from flask import Blueprint
from Middleware.Meta.Middleware import Middleware

from DataHandler import DataHandler


class Behavior(ABC):
    @abstractmethod
    def __init__(self, route: str, data_handler: type[DataHandler], **args):
        ...

    @abstractmethod
    def _bind(self, bp: Blueprint):
        ...

    def bind(self, bp: Blueprint, middleware: list[Middleware] = []):
        for midware_defs in middleware:
            initilized = midware_defs["class"](**midware_defs["args"])
            bp.before_request(initilized._run)

        self._bind(bp)
