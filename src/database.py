from pymongo import MongoClient

from src.config import MONGO_DATABASE, MONGO_URL
from src.decorators import DatabaseWrapper
from src.utils import Singleton


class Database(metaclass=Singleton):
    def __init__(self):
        self.db = None
        self.client = None

    def _lazy_init(self):
        """
        We do not want to initialize the database during module import.
        """
        self.client = MongoClient(MONGO_URL, w=3, tlsAllowInvalidCertificates=True)
        mongo_db = self.client.get_database(MONGO_DATABASE)
        self.db = DatabaseWrapper(mongo_db)

    def __call__(self):
        if self.db is None:
            self._lazy_init()
        return self.db


db = Database()
db()
