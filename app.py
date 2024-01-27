from flask import Flask

from flask_restful import Api
from flask_apispec import FlaskApiSpec, marshal_with
from flask_admin import Admin
from flask_peewee.db import Database

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from config import DebugConfig

from admin.views import add_views

from api.auth import register_auth_api
from api.bills import register_bills_api

from data.models import User, Bill, BillItem
from data.schemas import ErrorSchema

app = Flask(__name__)
api = Api(app)

app.config.from_object(DebugConfig())
    
db = Database(app)
db.database.bind([User])
db.database.create_tables([User])
db.database.bind([Bill])
db.database.create_tables([Bill])
db.database.bind([BillItem])
db.database.create_tables([BillItem])

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='friendly_bill',
        version='v1',
        openapi_version='3.0.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})
docs = FlaskApiSpec(app, document_options=False)

app.config['FLASK_ADMIN_SWATCH'] = 'united'
admin = Admin(app, name='friendly_bill', template_mode='bootstrap3')
add_views(admin=admin)

register_bills_api(app, docs)
register_auth_api(app, docs)

@app.errorhandler(500)
@marshal_with(ErrorSchema)
def handle_server_error(err):
    error = {"message": str(err)}
    return error, 500

@app.errorhandler(422)
@marshal_with(ErrorSchema)
def handle_unprocessable_error(err):
    error = {"message": str(err)}
    return error, 422
    