from .Meta.Middleware import Middleware

from flask import session, Response
from json import load

from hashlib import pbkdf2_hmac


admin_file = open("./admin.json", 'r')
admin = load(admin_file)
admin_file.close()


def auth():
    try:
        uname = session["username"]
        passwd = session["password"]
    except KeyError:
        return Response(status = 403)

    key = admin["password"]
    salt = admin["salt"]

    in_key = pbkdf2_hmac('sha256', passwd.encode(), salt.encode(), 100000)

    if in_key.hex() != key or admin["username"] != uname:
        return Response(status = 403)


class BasicAuth(Middleware):
    def __init__(self, **args):
        admin_file_path = args["admin_file_path"]

        admin_file = open(admin_file_path)
        self.admin_data = load(admin_file)
        admin_file.close()

        super().__init__(**args)

    def _run(self):
        try:
            uname = session["username"]
            passwd = session["password"]
        except KeyError:
            return Response(status = 403)

        key = admin["password"]
        salt = admin["salt"]

        in_key = pbkdf2_hmac('sha256', passwd.encode(), salt.encode(), 100000)

        if in_key.hex() != key or admin["username"] != uname:
            return Response(status = 403)
