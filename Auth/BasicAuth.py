from flask import session, request, Response


def auth():
    username = request.get_json()["username"]
    if username not in session["username"]:
        return Response(status = 403)
