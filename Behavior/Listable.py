from .Indexable import Indexable

from flask import Blueprint, request

from os import listdir


class Listable(Indexable):
    """
    Behavior for data that can be listed,
    allowing for manipulations such as sorting.
    """
    def __init__(self, route: str, files: [], header_file: str):
        super().__init__(route, files)
        self.header_file = header_file

    def get_all_data(self, sort_data: bool) -> []:
        data = map(int, listdir(self.route))

        if sort_data:
            return sorted(data)
        return data

    def get_header_data(self) -> []:
        headers = []
        sort_data = request.args.get("sort", True, bool)

        data = self.get_all_data(sort_data)

        for i in data:
            header = self.get_data_for_index(i)
            headers.append(header[self.header_file])

        final_data = {
            "headers": headers,
            "indecies": list(data)
        }

        return final_data

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("",
            view_func = self.get_header_data,
            methods = ['GET']
        )

        super()._bind(bp)
