from flask import Blueprint, Flask
from Behavior import mapper, Behavior

from Middleware.Meta.Middleware import Middleware
from Middleware.BasicAuth import BasicAuth

from .Importer import handle_imports
from DataHandler import *


def _get_behavior(name: str, behaviors: list, init_params: dict) -> Behavior:
    types = []
    for behavior in behaviors:
        types.append(mapper[behavior])

    view = type(name, tuple(types), {})
    return view(**init_params)


def get_bp(name: str, init_params: dict, cont: dict, middleware: list[Middleware] = []) -> Blueprint:
    bp = Blueprint(name, __name__, url_prefix = '/' + init_params["rest_path"])
    del init_params["rest_path"]

    view_obj = _get_behavior(name, cont["names"], init_params)

    view_obj.bind(bp, middleware)

    return bp


def build_modules(imports):
    imported = handle_imports(imports)
    built_in = {
        "data_handler": {
            "filesys": FilesysData,
            "sqlite": SQLiteData
        },
        "middleware": {
            "basic_auth": BasicAuth
        }
    }

    modules = {}

    for key, value in built_in.items():
        modules[key] = value | imported.get(key, {})

    modules = imported | modules

    return modules


def bind(app: Flask, config: dict):
    modules = build_modules(config.get("imports", {}))

    for model_name, model in config["models"].items():
        behaviors = model["behaviors"]

        init = behaviors["init"]
        middleware = behaviors.get("middleware", {})

        # Routing is all screwed up???
        init["route"] = f"{config['data_root']}/{model['route']}"
        init["rest_path"] = model['route']
        init["data_handler"] = modules["data_handler"][model["data_handler"]]

        for cont_name, cont in behaviors["containers"].items():
            spec_init = cont.get("init", {}) | init
            spec_middleware = cont.get("middleware", {}) | middleware

            middleware_funcs = [{"class": modules["middleware"][name], "args": args} for name, args in spec_middleware.items()]

            bp_name = model_name + '_' + cont_name
            app.register_blueprint(get_bp(bp_name, spec_init, cont, middleware_funcs))
