from Binders.ConfigBinder import bind

from flask import Flask
from flask_cors import CORS

from json import load

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

config = None

with open("config.json", 'r') as conf_file:
    config = load(conf_file)

bind(app, config)
print(app.url_map)

app.run()
