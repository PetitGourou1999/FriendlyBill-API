from flask_login import current_user
from flask_admin.contrib.peewee import ModelView

from wtforms import fields, validators

from shortcuts import encrypt_password

from data.models import User, OTP, Bill, BillUser, BillItem

class UsersView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

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


class OTPsView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    can_view_details = True
    can_export = True

    form_args = {
        'user': {
            'validators': [validators.InputRequired()]
        },
    }


class BillsView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    can_view_details = True
    can_export = True

    form_args = {
        'title': {
            'validators': [validators.InputRequired()]
        },
    }


class BillUsersView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    can_view_details = True
    can_export = True

    form_args = {
        'user': {
            'validators': [validators.InputRequired()]
        },
        'bill': {
            'validators': [validators.InputRequired()]
        },
    }


class BillItemsView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    can_view_details = True
    can_export = True

    form_args = {
        'title': {
            'validators': [validators.InputRequired()]
        },
        'user': {
            'validators': [validators.InputRequired()]
        },
    }


def add_admin_views(admin):
    admin.add_view(UsersView(User))
    admin.add_view(OTPsView(OTP))
    admin.add_view(BillsView(Bill))
    admin.add_view(BillUsersView(BillUser))
    admin.add_view(BillItemsView(BillItem))
