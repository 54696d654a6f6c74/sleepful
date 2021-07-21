from abc import ABC, abstractclassmethod
from flask import Blueprint
from typing import Callable


class Behavior(ABC):
    @abstractclassmethod
    def _bind(self, bp: Blueprint):
        raise NotImplementedError

    def bind(self, bp: Blueprint, auth: Callable = None, **auth_opts):
        if auth is not None:
            bp.before_request(lambda: auth(**auth_opts))
            pass

        self._bind(bp)
