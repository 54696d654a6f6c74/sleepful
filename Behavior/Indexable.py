from flask import Blueprint, Response

from Behavior import Behavior
from DataHandler import DataHandler


class Indexable(Behavior):
    """
    Behavior for data that can be accessed
    via enumerable indices
    """
    def __init__(self, route: str, data_handler: type[DataHandler], **args):
        self.data_handler = data_handler
        self.route = route

        self.fields = args["fields"]

    def get_data_for_index(self, index: int):
        data_dict = {}

        with self.data_handler(self.route) as handler:
            try:
                data_dict = handler.get_data_fields(index, self.fields)
            except AttributeError:
                return Response(status = 404)

        return data_dict

    def get_data_for_item(self, index: int, file_name: str):
        data = {}

        try:
            with self.data_handler(self.route) as handler:
                data = handler.get_data_field(index, file_name)
        except FileNotFoundError:
            return Response(status = 404)

        return data

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("/<int:index>",
            view_func = self.get_data_for_index,
            methods = ['GET']
        )

        bp.add_url_rule("/<int:index>/<string:file_name>",
            view_func = self.get_data_for_item,
            methods = ['GET']
        )
