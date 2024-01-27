from marshmallow import *

class BaseSchema(Schema):
    created_date = fields.DateTime(dump_only=True)
    updated_date = fields.DateTime(dump_only=True)

    class Meta:
        dateformat = '%Y-%m-%dT%H:%M:%S'


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


    class Meta(BaseSchema.Meta):
        additional = ('duration',)
        ordered = True


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserTokenSchema(Schema):
    user = fields.Nested(UserSchema)
    token = fields.Str()


class BillSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    
    class Meta(BaseSchema.Meta):
        additional = ('duration',)
        ordered = True
    

class BillItemSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    user = fields.Nested(UserSchema)
    bill = fields.Nested(BillSchema)

    class Meta(BaseSchema.Meta):
        additional = ('duration',)
        ordered = True


class ErrorSchema(Schema):
    message = fields.Str(metadata={"default": "An error occurred"})