import pytest
from flask import Flask
from service.server import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.app_context():
        yield app.test_client()

def test_request_example(client):
    response = client.get("/ping")
    assert b"Cats Service. Version 0.1" in response.data



"""


def test_get_cats(client):
    response = client.get("/cats")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Cats!"
"""