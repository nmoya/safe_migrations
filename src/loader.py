from os import listdir
from os.path import isfile, join


def load_migration_files(path):
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def load_migration_modules(path):
    return [f.replace("/", ".") for f in load_migration_files(path)]


def import_method_by_module_str(full_name, direction):
    function_path = full_name.replace("py", direction)
    module_name, unit_name = function_path.rsplit(".", 1)
    return getattr(__import__(module_name, fromlist=[""]), unit_name)
