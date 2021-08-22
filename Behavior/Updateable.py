from .Indexable import Indexable

from flask import Response, Blueprint, request

from json import dumps


class Updateable(Indexable):
    def update_file(self, file_name: str, index: int) -> Response:
        data = request.get_json()
        data_to_write = dumps(data[file_name])

        try:
            with self.data_handler(self.route) as handler:
                handler.updata_data(index, file_name, data_to_write)

        except FileNotFoundError:
            return Response(status = 404)

        return Response(status = 200)

    def update_all_files(self, index: int) -> Response:
        data = request.get_json()

        try:
            with self.data_handler(self.route) as handler:
                handler.update_multiple(index, self.fields, data)

        except FileNotFoundError:
            return Response(status = 404)

        return Response(status = 200)

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("/<int:index>",
            view_func = self.update_all_files,
            methods = ['PUT']
        )

        bp.add_url_rule("/<int:index>/<string:file_name>",
            view_func = self.update_file,
            methods = ['PUT']
        )

        super()._bind(bp)
