from flask import Flask


class Context:
    app = Flask(__name__)


ctx = Context()
