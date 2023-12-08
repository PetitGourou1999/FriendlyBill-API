class DefaultConfig(object):
    DEBUG = False
    DATABASE = {
        'name': 'database.db',
        'engine': 'peewee.SqliteDatabase'
    }


class DebugConfig(object):
    DEBUG = True
    DATABASE = {
        'name': 'database.db',
        'engine': 'peewee.SqliteDatabase'
    }


class TestingConfig(object):
    DEBUG = True
    DATABASE = {
        'name': ':memory:',
        'engine': 'peewee.SqliteDatabase'
    }
    TESTING = True

