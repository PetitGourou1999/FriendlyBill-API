from datetime import datetime

from flask import request
from flask.views import MethodView

class ItemView(MethodView):
    init_every_request = False

    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def _get_item(self, id):
        return self.model.get_or_none(self.model.id == id)

    def get(self, id):
        item = self._get_item(id)
        if item:
            return self.schema.dump(item), 200
        else:
            return 'Item not found', 404

    def put(self, id):
        item = self._get_item(id)
        if item:
            new_data = request.json
            for attr in new_data:
                if hasattr(item, attr):
                    if isinstance(getattr(item, attr), datetime):
                        setattr(item, attr, datetime.fromisoformat(new_data[attr]))
                    else:
                        setattr(item, attr, new_data[attr])
            item.save()
            return self.schema.dump(item), 200
        else:
            return 'Item not found', 404

    def delete(self, id):
        item = self._get_item(id)
        if item:
            item.delete_instance()
            return '', 200
        else:
            return 'Item not found', 404


class GroupView(MethodView):
    init_every_request = False

    def __init__(self, model, schema, schemas):
        self.model = model
        self.schema = schema
        self.schemas = schemas

    def get(self):
        items = self.model.select()
        return self.schemas.dump(items), 200

    def post(self):
        try:
            new_data = request.json
            item = self.model.create(**new_data)
            return self.schema.dump(item), 201
        except Exception as e:
            return str(e), 400


def register_api(app, model, url, schema, schemas):
    item = ItemView.as_view(f"{url}-apiitemview", model, schema)
    app.add_url_rule(f"/api/{url}/<int:id>", view_func=item)
    group = GroupView.as_view(f"{url}s-apigroupview", model, schema, schemas)
    app.add_url_rule(f"/api/{url}s/", view_func=group)
