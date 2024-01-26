from flask_admin.contrib.peewee import ModelView

from data.models import User, Bill, BillItem

class UsersView(ModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['email', ]

    can_view_details = True


class BillsView(ModelView):    
    can_view_details = True


class BillItemsView(ModelView):    
    can_view_details = True


def add_views(admin):
    admin.add_view(UsersView(User))
    admin.add_view(BillsView(Bill))
    admin.add_view(BillItemsView(BillItem))
