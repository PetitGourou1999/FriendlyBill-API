from datetime import datetime

from flask import request
from flask.views import MethodView

from api.decorators import token_required

class ItemView(MethodView):
    init_every_request = False

    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def _get_item(self, id):
        return self.model.get_or_none(self.model.id == id)

    @token_required
    def get(self, id):
        item = self._get_item(id)
        if not item:
            return {
                "message": "Item not found"
            }, 400
        return self.schema.dump(item), 200
            
    @token_required
    def put(self, id):
        item = self._get_item(id)
        if not item:
            return {
                "message": "Item not found"
            }, 400
        new_data = request.json
        if not new_data:
            return {
                "message": "Please provide details",
            }, 400
        for attr in new_data:
            if hasattr(item, attr):
                if isinstance(getattr(item, attr), datetime):
                    setattr(item, attr, datetime.fromisoformat(new_data[attr]))
                else:
                    setattr(item, attr, new_data[attr])
        item.save()
        return self.schema.dump(item), 200
        
    @token_required
    def delete(self, id):
        item = self._get_item(id)
        if not item:
            return {
                "message": "Item not found"
            }, 400
        item.delete_instance()
        return {}, 200

class GroupView(MethodView):
    init_every_request = False

    def __init__(self, model, schema, schemas):
        self.model = model
        self.schema = schema
        self.schemas = schemas

    @token_required
    def get(self):
        items = self.model.select()
        return self.schemas.dump(items), 200

    @token_required
    def post(self):
        new_data = request.json
        if not new_data:
            return {
                "message": "Please provide details",
            }, 400    
        try:
            item = self.model.create(**new_data)
            return self.schema.dump(item), 201
        except Exception as e:
            return {
                "message:": str(e)
            }, 400


def register_api(app, model, url, schema, schemas):
    item = ItemView.as_view(f"{url}-apiitemview", model, schema)
    app.add_url_rule(f"/api/{url}/<int:id>", view_func=item)
    group = GroupView.as_view(f"{url}s-apigroupview", model, schema, schemas)
    app.add_url_rule(f"/api/{url}s/", view_func=group)
