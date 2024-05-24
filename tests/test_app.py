import pytest
from service.server import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.app_context():
        yield app.test_client()


def test_request_example(client):
    response = client.get("/ping")
    assert b"Cats Service. Version 0.1" in response.data


def test_get_cats(client):
    response = client.get("/cats")
    assert response.status_code == 200
    response = client.get("/cats?attribute=name&order=asc")
    assert response.status_code == 200
    response = client.get("/cats?attribute=tail_length&order=desc")
    assert response.status_code == 200
    response = client.get("/cats?attribute=color&order=asc&offset=5&limit=2")
    assert response.status_code == 200


def test_post_cats(client):
    post_data = "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
    response = client.post("/cat", post_data)
    assert response.status_code == 200


def test_limiter(client):
    response = client.get("/ping")
    assert response.status_code == 200
    for i in range(600):
        client.get("/ping")
    print(client.get("/ping").get_data())
    assert b"429 Too Many Requests" in client.get("/ping").data
