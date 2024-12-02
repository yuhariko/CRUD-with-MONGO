from pymongo import MongoClient
from config import config_object

class MongoDBController:
    def __init__(self):
        self.connection_string = config_object.MONGO_URI
        self.db_name = config_object.ADMIN_DB

    def __enter__(self):
        self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=50000)
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()


