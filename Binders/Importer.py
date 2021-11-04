from importlib.util import spec_from_file_location, module_from_spec


def get_module(module_name: str, module_path: str):
    spec = spec_from_file_location(module_name, module_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, module_name)


def handle_imports(imports: dict) -> dict:
    proccessed = {}

    for key, values in imports.items():
        proccessed[key] = {}

        for value in values:
            mod_name = value["module_name"]
            mod_path = value["path"]

            mod = get_module(mod_name, mod_path)

            proccessed[key][value["name"]] = mod

    return proccessed
