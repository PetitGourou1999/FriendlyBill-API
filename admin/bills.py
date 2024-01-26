from flask_admin.contrib.peewee import ModelView

class BillsView(ModelView):    
    can_view_details = True
