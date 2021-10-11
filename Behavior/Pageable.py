from .Listable import Listable
from Pagination.pagelist import Pagelist

from flask import request, Blueprint

from DataHandler import DataHandler

from math import ceil


class Pageable(Listable):
    """
    Behavior for listable data that
    supports pagination
    """
    def __init__(self, route: str, data_handler: type[DataHandler], **args):
        super().__init__(route, data_handler, **args)
        self.page_size = args["page_size"]

    def get_all_data(self, sort_data: bool) -> list:
        data = super().get_all_data(sort_data)

        if request.args.get('all', False, bool) is True:
            return data

        page = request.args.get('page', 1, int)

        try:
            items = Pagelist(self.page_size, data)

            return items.get_page(page - 1)
        except IndexError:
            return []

    def get_page_count(self) -> int:
        data = list(super().get_all_data(False))
        print(data)
        pages = ceil(len(data) / self.page_size)

        return {
            "pages": pages
        }

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("/pages",
            view_func = self.get_page_count,
            methods = ['GET']
        )

        super()._bind(bp)
