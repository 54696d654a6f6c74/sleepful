from typing import Callable
from flask import Blueprint, Flask
from Behavior import mapper, Behavior

from Middleware.BasicAuth import auth

from .Importer import handle_imports
from DataHandler import *


def _get_behavior(name: str, behaviors: list, init_params: dict) -> Behavior:
    types = []
    print(init_params)
    for behavior in behaviors:
        types.append(mapper[behavior])

    view = type(name, tuple(types), {})
    return view(**init_params)


def get_bp(name: str, init_params: dict, cont: dict, middleware: list[Callable] = []) -> Blueprint:
    bp = Blueprint(name, __name__, url_prefix = '/' + init_params["route"])
    # del init_params["route"]

    view_obj = _get_behavior(name, cont["names"], init_params)

    for func in middleware:
        view_obj.bind(bp, func)

    return bp


def build_modules(imports):
    imported = handle_imports(imports)
    built_in = {
        "data_handler": {
            "filesys": FilesysData,
            "sqlite": SQLiteData
        },
        "middleware": {
            "basic_auth": auth
        }
    }

    modules = {}

    for key, value in built_in.items():
        modules[key] = value | imported.get(key, {})

    modules = imported | modules

    return modules


def bind(app: Flask, config: dict):
    modules = build_modules(config["imports"])

    for model_name, model in config["models"].items():
        behaviors = model["behaviors"]

        init = behaviors["init"]
        middleware = behaviors.get("middleware", [])

        init["route"] = f"{config['data_root']}/{model['route']}"
        init["data_handler"] = modules["data_handler"][model["data_handler"]]

        for cont_name, cont in behaviors["containers"].items():
            spec_init = cont.get("init", {}) | init
            spec_middleware = list(set(cont.get("middleware", []) + middleware))

            middleware_funcs = [modules["middleware"][name] for name in spec_middleware]

            bp_name = model_name + '_' + cont_name
            app.register_blueprint(get_bp(bp_name, spec_init, cont, middleware_funcs))
