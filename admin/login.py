from flask import request, url_for, redirect
from flask_login import login_user, logout_user, current_user
from flask_admin import AdminIndexView
from flask_admin import helpers, expose

from wtforms import form, fields, validators

from data.models import User

from shortcuts import check_password

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()
            form.populate_obj(user)
            User.create(**user.__data__)

            login_user(user)
            return redirect(url_for('.index'))
        
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


class LoginForm(form.Form):
    email = fields.EmailField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid credentials')

        if not check_password(self.password.data, user.password):
            raise validators.ValidationError('Invalid credentials')

    def get_user(self):
        return User.get_by_email(self.email.data)


class RegistrationForm(form.Form):
    firstname = fields.StringField(validators=[validators.InputRequired()])
    surname = fields.StringField(validators=[validators.InputRequired()])
    email = fields.EmailField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        if User.get_by_email(self.email.data) is not None:
            raise validators.ValidationError('Email already taken')