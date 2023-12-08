from marshmallow import *

from models.user import User

class UserSchema(Schema):
    id = fields.Int()
    firstname = fields.Str()
    surname = fields.Str()
    email = fields.Str()
    created_date = fields.Str()
    updated_date = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return User(**data)
