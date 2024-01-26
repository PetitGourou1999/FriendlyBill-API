from flask_admin.contrib.peewee import ModelView

class UsersView(ModelView):
    column_exclude_list = ['password', ]

    can_view_details = True

