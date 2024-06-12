from logzero import logger

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
        
        try:
            form.validate_login()
            user = form.get_user()
            login_user(user)
        except validators.ValidationError as error:
            self._template_args['validation_error'] = error
            logger.warn(str(error))

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        
        self._template_args['form'] = form

        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


class LoginForm(form.Form):
    email = fields.EmailField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self):
        user = self.get_user()
        
        if user is None:
            logger.info('LoginForm >>> user <%s> does not exists', self.email.data)
            raise validators.ValidationError('Invalid credentials')
        
        if not user.is_superadmin:
            logger.info('LoginForm >>> user <%s> is not an admin', self.email.data)
            raise validators.ValidationError('Invalid credentials')

        if not check_password(self.password.data, user.password):
            logger.info('LoginForm >>> user password is invalid')
            raise validators.ValidationError('Invalid credentials')

    def get_user(self):
        return User.get_by_email(self.email.data)