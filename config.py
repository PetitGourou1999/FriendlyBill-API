import os

class DefaultConfig(object):
    DEBUG = False
    DATABASE = {
        'name': 'database.db',
        'engine': 'peewee.SqliteDatabase'
    }
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DebugConfig(object):
    DEBUG = True
    DATABASE = {
        'name': 'database.db',
        'engine': 'peewee.SqliteDatabase'
    }
    SECRET_KEY = 'SuperSecret'


class TestingConfig(object):
    DEBUG = True
    DATABASE = {
        'name': ':memory:',
        'engine': 'peewee.SqliteDatabase'
    }
    SECRET_KEY = 'SuperSecret'
    TESTING = True

