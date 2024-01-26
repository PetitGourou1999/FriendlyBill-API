from flask_admin.contrib.peewee import ModelView

class BillItemsView(ModelView):    
    can_view_details = True
