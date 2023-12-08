from marshmallow import *

from models.bill_item import BillItem

from schemas.user import UserSchema
from schemas.bill import BillSchema

class BillItemSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    created_date = fields.Str()
    updated_date = fields.Str()
    user = fields.Nested(UserSchema)
    bill = fields.Nested(BillSchema)

    @post_load
    def make(self, data, **kwargs):
        return BillItem(**data)
