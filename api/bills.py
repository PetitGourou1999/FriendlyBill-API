from flask_apispec import use_kwargs, marshal_with, doc
from flask_apispec.views import MethodResource

from webargs import fields

from data.models import Bill, BillItem
from data.schemas import BillSchema, BillItemSchema, ErrorSchema

from api.decorators import token_required

class BillResource(MethodResource):

    def _get_item(self, id) -> Bill:
        return Bill.get_or_none(Bill.id == id)

    @token_required
    @use_kwargs({'id': fields.Int()}, location='query')
    @marshal_with(BillSchema, code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Get bill info', tags=['Bills'])
    def get(self, **kwargs):
        bill = self._get_item(kwargs.get('id'))
        if not bill:
            error = {"message": "Bill not found"}
            return error, 400
        return bill, 200
    
    @token_required
    @use_kwargs(BillSchema, location='json')
    @marshal_with(BillSchema, code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Create bill', tags=['Bills'])
    def post(self, **kwargs):
        if not kwargs:
            error = {"message": "Please provide details"}
            return error, 400
        try:
            bill = Bill.create(**kwargs)
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return bill, 200
    
    @token_required
    @use_kwargs({'id': fields.Int()}, location='query')
    @marshal_with(BillSchema, code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Delete bill', tags=['Bills'])
    def delete(self, **kwargs):
        bill = self._get_item(kwargs.get('id'))
        if not bill:
            error = {"message": "Bill not found"}
            return error, 400
        try:
            bill.delete()
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return {}, 204


class BillItemResource(MethodResource):

    def _get_item(self, id) -> BillItem:
        return BillItem.get_or_none(BillItem.id == id)

    @token_required
    @use_kwargs({'id': fields.Int()}, location='query')
    @marshal_with(BillItemSchema, code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Get bill item info', tags=['Bill Items'])
    def get(self, **kwargs):
        bill_item = self._get_item(kwargs.get('id'))
        if not bill_item:
            error = {"message": "Bill Item not found"}
            return error, 400
        return bill_item, 200
    
    @token_required
    @use_kwargs(BillItemSchema, location='json')
    @marshal_with(BillItemSchema, code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Create bill item', tags=['Bill Items'])
    def post(self, **kwargs):
        if not kwargs:
            error = {"message": "Please provide details"}
            return (error, 400)
        try:
            bill_item = BillItem.create(**kwargs)
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return bill_item, 200
    
    @token_required
    @use_kwargs({'id': fields.Int()}, location='query')
    @marshal_with(BillItemSchema, code=200)
    @marshal_with(ErrorSchema, code=400)
    @doc(description='Delete bill item', tags=['Bill Items'])
    def delete(self, **kwargs):
        bill_item = self._get_item(kwargs.get('id'))
        if not bill_item:
            error = {"message": "Bill Item not found"}
            return error, 400
        try:
            bill_item.delete()
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        return {}, 204


def register_bills_api(application, docs):
    application.add_url_rule('/api/bills', view_func=BillResource.as_view('Bill'))
    application.add_url_rule('/api/bill-items', view_func=BillItemResource.as_view('BillItem'))

    docs.register(BillResource, endpoint='Bill')
    docs.register(BillItemResource, endpoint='BillItem')