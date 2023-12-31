from marshmallow import *

from models.bill_item import BillItem

from schemas.user import UserSchema
from schemas.bill import BillSchema

class BillItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    created_date = fields.DateTime()
    updated_date = fields.DateTime()
    user = fields.Nested(UserSchema)
    bill = fields.Nested(BillSchema)

    @post_load
    def make(self, data, **kwargs):
        return BillItem(**data)
