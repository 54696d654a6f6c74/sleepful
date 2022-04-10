from Context import ctx

from .Meta.Middleware import Middleware

from flask import session, request, Response
from json import load

from hashlib import pbkdf2_hmac


class BasicAuth(Middleware):
    def __init__(self, **args):
        admin_file_path = args["admin_file_path"]

        admin_file = open(admin_file_path)
        self.admin_data = load(admin_file)
        admin_file.close()

        super().__init__(**args)

    @ctx.app.route("/login", endpoint = "login", methods = ['POST'])
    def login(self):
        try:
            username = request.get_json()["username"]
            password = request.get_json()["password"]

            session["username"] = username
            session["password"] = password
        except KeyError:
            return Response(status = 400)
        return Response(status = 200)

    def _run(self):
        try:
            uname = session["username"]
            passwd = session["password"]
        except KeyError:
            return Response(status = 403)

        key = self.admin_data["password"]
        salt = self.admin_data["salt"]

        in_key = pbkdf2_hmac('sha256', passwd.encode(), salt.encode(), 100000)

        if in_key.hex() != key or self.admin_data["username"] != uname:
            return Response(status = 403)
