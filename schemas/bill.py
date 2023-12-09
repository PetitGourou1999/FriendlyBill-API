from marshmallow import *

from models.bill import Bill

class BillSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    created_date = fields.Str()
    updated_date = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return Bill(**data)
