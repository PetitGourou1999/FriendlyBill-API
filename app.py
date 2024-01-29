import click

import logzero

from flask import Flask
from flask import render_template

from flask_restful import Api
from flask_apispec import FlaskApiSpec, marshal_with
from flask_admin import Admin
from flask_login import LoginManager
from flask_peewee.db import Database

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from config import DebugConfig

from admin.login import MyAdminIndexView
from admin.views import add_admin_views

from api.auth import register_auth_api
from api.bills import register_bills_api

from commands import create_admin

from data.models import User, Bill, BillItem
from data.schemas import ErrorSchema

# Init App
app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def get(): 
    return render_template('index.html')

app.config.from_object(DebugConfig())

# Init logging
logzero.logfile('logs/friendly_bill.log')

# Init Database
db = Database(app)
db.database.bind([User])
db.database.create_tables([User])
db.database.bind([Bill])
db.database.create_tables([Bill])
db.database.bind([BillItem])
db.database.create_tables([BillItem])

# Init Swagger
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

# Init Admin
app.config['FLASK_ADMIN_SWATCH'] = 'lux'
admin = Admin(app, name='friendly_bill', index_view=MyAdminIndexView(), template_mode='bootstrap4')
add_admin_views(admin=admin)

# Init Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

# Register Ressources
register_bills_api(app, docs)
register_auth_api(app, docs)

# Register cli commands
@app.cli.command('admin', help='Manage admin user')
@click.option('--create', help='Add admin user', is_flag=True)
def manage_admin(create):
    if create:
        create_admin()

# Error Handlers
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
    