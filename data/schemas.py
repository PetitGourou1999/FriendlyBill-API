from marshmallow import *

from data.models import User, Bill, BillItem

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email()
    password = fields.Str(required=True, load_only=True)
    
    @post_load
    def make(self, data, **kwargs):
        return User(**data)


class BillSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    created_date = fields.DateTime()
    updated_date = fields.DateTime()

    @post_load
    def make(self, data, **kwargs):
        return Bill(**data)


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
