from logzero import logger

from flask_apispec import use_kwargs, marshal_with, doc
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required, current_user

from data.models import User, Bill, BillUser, BillItem
from data.schemas import BillUserSchema, BillItemSchema, ErrorSchema
from data.schemas import CreateBillSchema, InviteUserSchema, CreateBillItemSchema

class BillResource(MethodResource):

    @jwt_required()
    @marshal_with(BillUserSchema(many=True), code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Get bills', tags=['Bills'])
    def get(self):
        bills = BillUser.get_by_user(current_user)
        if not bills:
            error = {"message": "Bills not found"}
            return error, 400
        return bills, 200
    
    @jwt_required()
    @use_kwargs(CreateBillSchema, location='json')
    @marshal_with(ErrorSchema, code=400)
    @marshal_with(ErrorSchema, code=500)
    @doc(description='Create bill', tags=['Bills'])
    def post(self, **kwargs):
        if not kwargs:
            error = {"message": "Please provide details"}
            return error, 400
        try:
            bill = Bill.create(title=kwargs.get('title'))
            BillUser.create(user=current_user, bill=bill, is_owner=True)
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return {}, 201
    

class BillUserResource(MethodResource):

    @jwt_required()
    @use_kwargs(InviteUserSchema, location='json')
    @marshal_with(ErrorSchema, code=400)
    @marshal_with(ErrorSchema, code=500)
    @doc(description='Invite user', tags=['Bill Users'])
    def post(self, **kwargs):
        if not kwargs:
            error = {"message": "Please provide details"}
            return error, 400
        invited = User.get_by_email(kwargs.get('user_email'))
        if not invited:
            error = {"message": "User does not exist"}
            return error, 400
        bill = Bill.get_or_none(Bill.id == kwargs.get('bill_id'))
        if not bill:
            error = {"message": "Bill does not exist"}
            return error, 400
        bill_owner = BillUser.get_by_user_and_bill(current_user, bill)
        if not bill_owner.is_owner:
            error = {"message": "You are not the owner of this bill"}
            return error, 400
        bill_user = BillUser.get_by_user_and_bill(invited, bill)
        if bill_user:
            error = {"message": "User has already been invited"}
            return error, 400
        try:
            BillUser.create(user=invited, bill=bill, is_owner=False)
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return {}, 201
    

class BillItemResource(MethodResource):

    @jwt_required()
    @marshal_with(BillItemSchema(many=True), code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Get bill items', tags=['Bill Items'])
    def get(self):
        bill_items = BillItem.get_by_user(current_user)
        if not bill_items:
            error = {"message": "Bill Items not found"}
            return error, 400
        return bill_items, 200
    
    @jwt_required()
    @use_kwargs(CreateBillItemSchema, location='json')
    @marshal_with(ErrorSchema, code=400)
    @marshal_with(ErrorSchema, code=500)
    @doc(description='Create bill item', tags=['Bill Items'])
    def post(self, **kwargs):
        if not kwargs:
            error = {"message": "Please provide details"}
            return error, 400
        bill = Bill.get_or_none(Bill.id == kwargs.get('bill_id'))
        if not bill:
            error = {"message": "Bill does not exist"}
            return error, 400
        bill_user = BillUser.get_by_user_and_bill(current_user, bill)
        if not bill_user:
            error = {"message": "You cannot add items to this bill"}
            return error, 400
        try:
            BillItem.create(title=kwargs.get('title'), bill_user=bill_user)
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return {}, 201
    

def register_bills_api(application, docs):
    application.add_url_rule('/api/bills', view_func=BillResource.as_view('Bills'))
    application.add_url_rule('/api/bills/users', view_func=BillUserResource.as_view('BillUsers'))
    application.add_url_rule('/api/bills/items', view_func=BillItemResource.as_view('BillItems'))
    
    docs.register(BillResource, endpoint='Bills')
    docs.register(BillUserResource, endpoint='BillUsers')
    docs.register(BillItemResource, endpoint='BillItems')