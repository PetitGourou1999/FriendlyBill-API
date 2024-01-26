from flask import Flask
from flask_admin import Admin
from flask_peewee.db import Database

from config import DebugConfig

from blueprints import authentication
from views.generics import register_api

from models.models import User, Bill, BillItem
from schemas.schemas import BillSchema, BillItemSchema

from admin.views import UsersView, BillsView, BillItemsView

def init_db(application):
    database = Database(application)
    database.database.bind([User])
    database.database.create_tables([User])
    database.database.bind([Bill])
    database.database.create_tables([Bill])
    database.database.bind([BillItem])
    database.database.create_tables([BillItem])
    return database

def init_admin(application):
    application.config['FLASK_ADMIN_SWATCH'] = 'united'
    admin = Admin(application, name='friendly_bill', template_mode='bootstrap3')
    admin.add_view(UsersView(User))
    admin.add_view(BillsView(Bill))
    admin.add_view(BillItemsView(BillItem))

def put_in_register(application):
    register_api(application, Bill, "bill", BillSchema(), BillSchema(many=True))
    register_api(application, BillItem, "item", BillItemSchema(), BillItemSchema(many=True))
    application.register_blueprint(authentication.bp)

def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)
    init_db(application)
    init_admin(application)
    put_in_register(application)
    return application

if __name__ == '__main__':
    app = create_app(DebugConfig())
    app.run()
