from .Listable import Listable

from flask import Response, Blueprint, request


class Postable(Listable):
    def write_data(self) -> Response:
        data = request.get_json()

        with self.data_handler(self.route) as handler:
            handler.new_data(data)

        return Response(status = 201)

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("",
            view_func = self.write_data,
            methods = ['POST']
        )

        super()._bind(bp)
