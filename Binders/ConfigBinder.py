from flask import Blueprint, Flask
from Behavior import mapper


def bind(app: Flask, config: dict):
    for name, model in config["models"].items():
        bp = Blueprint(name, __name__, url_prefix = "/" + model["route"])

        behaviors = []
        for behavior in model["behaviors"]:
            behaviors.append(mapper[behavior])

        init = model["init_params"]

        init["route"] = config["data_root"] + "/" + model["route"]

        view = type(name, tuple(behaviors), {})
        obj = view(**init)

        obj.bind(bp)

        app.register_blueprint(bp)
