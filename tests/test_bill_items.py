import pytest

from config import TestingConfig
from app import create_app

from tests import data

from data.schemas import BillItemSchema

@pytest.fixture()
def app():
    app = create_app(TestingConfig())
    data.insert_data()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_events_get(client):
    response = client.get("/api/items/")
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    events = BillItemSchema(many=True).loads(response.text)
    assert len(events) == 1

