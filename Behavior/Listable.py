from .Indexable import Indexable

from flask import Blueprint, request

from DataHandler import DataHandler


class Listable(Indexable):
    """
    Behavior for data that can be listed,
    allowing for manipulations such as sorting.
    """
    def __init__(self, route: str, data_handler: type[DataHandler], **args):
        super().__init__(route, data_handler, **args)
        self.header_file = args["header_file"]

    def get_all_data(self, sort_data: bool) -> list:
        data = []
        with self.data_handler(self.route) as handler:
            data = handler.get_all_entry_indices(sort_data)

        return map(int, data)

    def get_header_data(self) -> list:
        headers = []
        sort_data = request.args.get("sort", True, bool)

        data = self.get_all_data(sort_data)

        for i in data:
            header = self.get_data_for_index(i)
            headers.append(header[self.header_file])

        final_data = {
            "headers": headers,
            "indices": list(data)
        }

        return final_data

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("",
            view_func = self.get_header_data,
            methods = ['GET']
        )

        super()._bind(bp)
