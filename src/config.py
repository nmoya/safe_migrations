import json

CONFIG_FILE = "migration_settings.json"


def config_content():
    with open("migration_settings.json") as config_fp:
        return json.loads(config_fp.read())


configs = config_content()
MONGO_URL = configs["MONGO_URL"]
MONGO_DATABASE = configs["MONGO_DATABASE"]
MIGRATIONS_ROOT = configs["MIGRATIONS_ROOT"]
TEST_DATABASE = configs["TEST_DATABASE"]
