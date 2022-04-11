from Context import ctx
from Binders.ConfigBinder import bind

from flask_cors import CORS
from flask_session import Session

from json import load

from os import urandom

ctx.app.config["DEBUG"] = True
ctx.app.config["SECRET_KEY"] = urandom(64)
ctx.app.config["SESSION_TYPE"] = "filesystem"
ctx.app.config["SESSION_COOKIE_SECURE"] = True
ctx.app.config["SESSION_COOKIE_SAMESITE"] = "None"

Session(ctx.app)
CORS(ctx.app)

config = None

with open("config.json", 'r') as conf_file:
    config = load(conf_file)

bind(ctx.app, config)
print(ctx.app.url_map)

ctx.app.run()
