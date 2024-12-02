import os


class Config:
    pass


class DevConfig(Config):
    if os.getenv('MONGO_URI'):
        MONGO_URI = os.getenv('MONGO_URI')
    else:
        MONGO_URI = "mongodb://localhost:27017/"

    ADMIN_DB = 'admin'
    DB_NAME = 'users'
    DEFAULT_PASSWORD = '123456'
    HOST_NAME = '0.0.0.0'
    PORT = 5000


config_object = DevConfig()
