from Binders.ConfigBinder import bind

from flask import Flask # , session, request, Response
from flask_cors import CORS
from flask_session import Session

from json import load

from os import urandom

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True

Session(app)
CORS(app)

config = None

with open("config.json", 'r') as conf_file:
    config = load(conf_file)

bind(app, config)
print(app.url_map)

app.run()
