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
    is_superadmin = fields.Bool()

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


class BillUserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    user = fields.Nested(UserSchema)
    bill = fields.Nested(BillSchema)
    is_owner = fields.Bool()

    class Meta(BaseSchema.Meta):
        additional = ('duration',)
        ordered = True


class CreateBillSchema(Schema):
    title = fields.Str(required=True)


class InviteUserSchema(Schema):
    user_email = fields.Email(required=True)
    bill_id = fields.Int(required=True)


class BillItemSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    amount = fields.Decimal(required=True, min=0)
    user = fields.Nested(BillUserSchema)
    
    class Meta(BaseSchema.Meta):
        additional = ('duration',)
        ordered = True


class CreateBillItemSchema(Schema):
    title = fields.Str(required=True)
    amount = fields.Decimal(required=True, min=0)
    bill_id = fields.Int(required=True)


class ErrorSchema(Schema):
    message = fields.Str(metadata={"default": "An error occurred"})