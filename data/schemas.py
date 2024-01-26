from marshmallow import *

from data.models import User, Bill, BillItem

class BaseSchema(Schema):
    created_date = fields.DateTime()
    updated_date = fields.DateTime()


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email()
    password = fields.Str(required=True, load_only=True)

    @post_load
    def make(self, data, **kwargs):
        return User(**data)


class BillSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    
    @post_load
    def make(self, data, **kwargs):
        return Bill(**data)


class BillItemSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    user = fields.Nested(UserSchema)
    bill = fields.Nested(BillSchema)

    @post_load
    def make(self, data, **kwargs):
        return BillItem(**data)


class ErrorSchema(Schema):
    message = fields.Str(metadata={"default": "An error occurred"})