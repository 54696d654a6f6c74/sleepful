from Behavior import Behavior

from DataHandler import DataHandler

from flask import session, request, Response, Blueprint


class Login(Behavior):
    def __init__(self, route: str, data_handler: type[DataHandler], **args):
        self.route = route
        self.data_handler = data_handler

    def login(self):
        try:
            username = request.get_json()["username"]
            password = request.get_json()["password"]

            session["username"] = username
            session["password"] = password
        except KeyError:
            return Response(status = 400)
        return Response(status = 200)

    def _bind(self, bp: Blueprint):
        bp.add_url_rule("/login",
            view_func = self.login,
            methods = ['POST']
        )
