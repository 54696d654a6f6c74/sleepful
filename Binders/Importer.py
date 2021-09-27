from importlib.util import spec_from_file_location, module_from_spec

from hashlib import pbkdf2_hmac
from secrets import token_urlsafe


def get_module(module_name: str, module_path: str):
    spec = spec_from_file_location(module_name, module_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def handle_imports(imports: dict) -> dict:
    proccessed = {}

    for key, value in imports.items():
        mod_name = value["module_name"]
        mod_path = value["path"]

        mod = get_module(mod_name, mod_path)

        proccessed[value["name"]] = mod

    return proccessed


def create_password_hash():
    password = b"h@rm@nl112"
    salt = token_urlsafe(64)

    dk = pbkdf2_hmac("sha256", password, salt.encode(), 100000)
    print(dk)
