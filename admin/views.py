from flask_admin.contrib.peewee import ModelView

from wtforms import fields, validators

from shortcuts import encrypt_password

from data.models import User, Bill, BillItem

class UsersView(ModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['email', ]

    can_view_details = True
    can_export = True

    form_overrides = {
        'email': fields.EmailField,
        'password': fields.PasswordField,
    }
    form_args = {
        'firstname': {
            'validators': [validators.InputRequired()]
        },
        'surname': {
            'validators': [validators.InputRequired()]
        },
        'email': {
            'validators': [validators.InputRequired()]
        },
        'password': {
            'validators': [validators.InputRequired()]
        }
    }

    def on_model_change(self, form, model, is_created):
        model.password = encrypt_password(model.password)
        return super().on_model_change(form, model, is_created)


class BillsView(ModelView):
    can_view_details = True
    can_export = True

    form_args = {
        'title': {
            'validators': [validators.InputRequired()]
        },
    }


class BillItemsView(ModelView):
    can_view_details = True
    can_export = True

    form_args = {
        'title': {
            'validators': [validators.InputRequired()]
        },
        'user': {
            'validators': [validators.InputRequired()]
        },
        'bill': {
            'validators': [validators.InputRequired()]
        },
    }



def add_views(admin):
    admin.add_view(UsersView(User))
    admin.add_view(BillsView(Bill))
    admin.add_view(BillItemsView(BillItem))
