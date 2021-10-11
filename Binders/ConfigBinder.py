from typing import Callable
from flask import Blueprint, Flask
from Behavior import mapper, Behavior

from Auth.BasicAuth import auth

from DataHandler import FilesysData


def _get_behavior(name: str, behaviors: list, init_params: dict) -> Behavior:
    types = []
    for behavior in behaviors:
        types.append(mapper[behavior])

    view = type(name, tuple(types), {})
    return view(**init_params)


def get_bp(name: str, model: dict, init_params: dict, prefix: str = "", auth_func: Callable = None, auth_params: dict = None) -> Blueprint:
    behaviors_key = prefix + "behaviors"
    type_name = prefix + name

    if behaviors_key in model:
        bp = Blueprint(type_name, __name__, url_prefix = "/" + model["route"])

        view_obj = _get_behavior(type_name, model[behaviors_key], init_params)
        if auth_params is not None:
            view_obj.bind(bp, auth_func, **auth_params)
        else:
            view_obj.bind(bp, auth_func or None)

        return bp


def bind(app: Flask, config: dict):
    for name, model in config["models"].items():
        model["init"]["route"] = f"{config['data_root']}/{model['route']}"
        model["init"]["data_handler"] = FilesysData # W.I.P

        init = model.get('init', {})

        auth_init = init | model.get('auth_init', {})
        non_auth_init = init | model.get('non_auth_init', {})

        app.register_blueprint(get_bp(name, model, non_auth_init))
        app.register_blueprint(get_bp(name, model, auth_init, "auth_", auth))
