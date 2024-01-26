from flask_admin.contrib.peewee import ModelView

class UsersView(ModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['email', ]

    can_view_details = True


class BillsView(ModelView):    
    can_view_details = True


class BillItemsView(ModelView):    
    can_view_details = True
