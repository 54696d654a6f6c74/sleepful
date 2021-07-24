from flask import Blueprint, Flask
from Behavior import mapper, Behavior

from Auth.BasicAuth import auth


def _get_behavior(name: str, behaviors: [], init_params: dict, bp: Blueprint) -> Behavior:
    types = []
    for behavior in behaviors:
        types.append(mapper[behavior])

    view = type(name, tuple(types), {})
    return view(**init_params)


def bind(app: Flask, config: dict):
    for name, model in config["models"].items():
        model["init_params"]["route"] = config["data_root"] + "/" + model["route"]

        auth_init = {}
        non_auth_init = {}

        if "non_auth" in model["init_params"]:
            non_auth_init = {}
            non_auth_init.update(model["init_params"]["non_auth"])

            del model["init_params"]["non_auth"]

        if "auth" in model["init_params"]:
            auth_init = {}
            auth_init.update(model["init_params"]["auth"])

            del model["init_params"]["auth"]

        if "behaviors" in model:
            bp = Blueprint(name, __name__, url_prefix = "/" + model["route"])

            non_auth_init.update(model["init_params"])
            print(non_auth_init)

            view_obj = _get_behavior(name, model["behaviors"], non_auth_init, bp)
            view_obj.bind(bp)

            app.register_blueprint(bp)

        if "auth_behaviors" in model:
            bp = Blueprint(name + "_auth", __name__, url_prefix = "/" + model["route"])

            auth_init.update(model["init_params"])

            view_obj = _get_behavior(name, model["auth_behaviors"], auth_init, bp)
            view_obj.bind(bp, auth)

            app.register_blueprint(bp)
