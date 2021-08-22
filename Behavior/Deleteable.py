from .Indexable import Indexable

from flask import Blueprint, Response


class Deleteable(Indexable):
    def delete_folder(self, index: int) -> Response:
        try:
            with self.data_handler(self.route) as handler:
                handler.remove_data(index)

        except FileNotFoundError:
            return Response(status = 404)

        return Response(status = 200)

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("/<int:index>",
            view_func = self.delete_folder,
            methods = ['DELETE']
        )

        super()._bind(bp)
