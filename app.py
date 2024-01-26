from flask import Flask
from flask_restful import Api
from flask_apispec import FlaskApiSpec
from flask_admin import Admin
from flask_peewee.db import Database

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from config import DebugConfig

from admin.views import add_views

from api import authentication
from api.resources import register_api

from data.models import User, Bill, BillItem

def init_db(application) -> Database:
    database = Database(application)
    database.database.bind([User])
    database.database.create_tables([User])
    database.database.bind([Bill])
    database.database.create_tables([Bill])
    database.database.bind([BillItem])
    database.database.create_tables([BillItem])
    return database

def init_admin(application) -> Admin:
    application.config['FLASK_ADMIN_SWATCH'] = 'united'
    admin = Admin(application, name='friendly_bill', template_mode='bootstrap3')
    add_views(admin=admin)
    return admin

def init_docs(application) -> FlaskApiSpec:
    application.config.update({
        'APISPEC_SPEC': APISpec(
            title='friendly_bill',
            version='v1',
            openapi_version='3.0.0',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
    })
    docs = FlaskApiSpec(application)
    return docs


def put_in_register(application, docs):
    register_api(application, docs)
    application.register_blueprint(authentication.bp)


def create_app(config):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config)
    
    db = init_db(app)
    docs = init_docs(app)
    admin = init_admin(app)

    put_in_register(app, docs)
    return app

if __name__ == '__main__':
    app = create_app(DebugConfig())
    app.run()
