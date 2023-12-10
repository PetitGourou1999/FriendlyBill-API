from marshmallow import *

from models.bill import Bill

class BillSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    created_date = fields.DateTime()
    updated_date = fields.DateTime()

    @post_load
    def make(self, data, **kwargs):
        return Bill(**data)
