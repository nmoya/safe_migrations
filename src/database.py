from pymongo import MongoClient

from src.config import MONGO_DATABASE, MONGO_URL
from src.decorators import DatabaseWrapper
from src.utils import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self, url, database):
        self.db = None
        self.client = None
        self.url = url
        self.database_name = database

    def _lazy_init(self):
        """
        We do not want to initialize the database during module import.
        """
        self.client = MongoClient(self.url, w=1, tlsAllowInvalidCertificates=True)
        database_ref = self.client.get_database(self.database_name)
        self.db = DatabaseWrapper(database_ref)

    def __call__(self):
        if self.db is None:
            self._lazy_init()
        return self.db


def main():
    db = DatabaseConnection(MONGO_URL, MONGO_DATABASE)
    db()
