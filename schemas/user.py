from marshmallow import *

from models.user import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email()
    password = fields.Str(required=True, load_only=True)
    
    @post_load
    def make(self, data, **kwargs):
        return User(**data)
