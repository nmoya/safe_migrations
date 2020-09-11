# type: ignore
import codecs
import functools
import json
import os
from glob import glob

import pymongo
import pytest
from bson import json_util

from src.config import MONGO_URL, TEST_DATABASE
from src.database import DatabaseConnection


def clean_database(db):
    for name in db.list_collection_names():
        db.drop_collection(name)


def load_fixture(db, collection, path):
    loader = functools.partial(json.load, object_hook=json_util.object_hook)
    with codecs.open(path, encoding="utf-8") as fp:
        docs = loader(fp)
        db[collection].insert_many(docs)


def load_fixtures(db):
    basedir = "tests/fixtures/mongodb"
    for file_name in glob(basedir + "/*.json"):
        collection, _ = os.path.splitext(os.path.basename(file_name))
        load_fixture(db, collection, file_name)


@pytest.fixture(scope="function", autouse=True)
def db():
    connection = DatabaseConnection(MONGO_URL, TEST_DATABASE)
    if "localhost" in MONGO_URL or "127.0.0.1" in MONGO_URL:
        clean_database(connection().db)
        load_fixtures(connection().db)
        yield connection
        clean_database(connection().db)
    else:
        yield connection
