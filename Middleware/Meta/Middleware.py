from abc import ABC, abstractclassmethod


class Middleware(ABC):
    @abstractclassmethod
    def __init__(self, **args):
        ...

    @abstractclassmethod
    def _run(self):
        ...

    def run(self):
        self._run()
