import os

class DefaultConfig(object):
    DEBUG = False
    DATABASE = {
        'name': 'database.db',
        'engine': 'peewee.SqliteDatabase'
    }
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


class DebugConfig(object):
    DEBUG = True
    DATABASE = {
        'name': 'database.db',
        'engine': 'peewee.SqliteDatabase'
    }
    SECRET_KEY = 'SuperSecret'
    JWT_SECRET_KEY = 'SuperSecretJWT'


class TestingConfig(object):
    DEBUG = True
    DATABASE = {
        'name': ':memory:',
        'engine': 'peewee.SqliteDatabase'
    }
    SECRET_KEY = 'SuperSecret'
    JWT_SECRET_KEY = 'SuperSecretJWT'
    TESTING = True

