import pytest
import json

from tests.helpers import create_item, create_headers
from main.schemas.item import ItemSchema


@pytest.mark.parametrize("credentials, category_id, data", [
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": "table", "description": "A table", "category_id": 1})])
def test_create_item_success(client, credentials, category_id, data):
    response, json_response = create_item(client, credentials,category_id, data)

    assert response.status_code == 201, "Successful create item should return 201"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


@pytest.mark.parametrize("credentials, category_id, data", [
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": "lamp", "description": "A table", "category_id": 1})])
def test_create_item_existed_item(client, credentials, category_id, data):
    response, json_response = create_item(client, credentials,category_id, data)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Item lamp already existed."
    assert json_response["error"] == {}


@pytest.mark.parametrize("credentials, category_id, data", [
    ({"username": "hizen2501", "password": "0123456"}, 1, {"description": "A table", "category_id": 1}),
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": "table", "category_id": 1}),
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": "table", "description": "A table", }),
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": 123123123, "description": "A table", "category_id": 1}),
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": "table", "description": 213123123, "category_id": 1}),
    ({"username": "hizen2501", "password": "0123456"}, 1, {"name": "table", "description": "A table", "category_id": "ewewf"})
])
def test_create_invalid_request_data(client, credentials, category_id, data):
    response, json_response = create_item(client, credentials, category_id, data)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_create_item_invalid_token(client):
    response = client.post("/categories/1/items", headers=create_headers(), data=json.dumps({"name": "lamp", "description": "A table", "category_id": 1}))
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credentials call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}


@pytest.mark.parametrize("credentials, category_id, data", [
    ({"username": "hizen2501", "password": "0123456"}, 100, {"name": "table", "description": "A table", "category_id": 100})])
def test_create_item_not_exist_category(client, credentials, category_id, data):
    response, json_response = create_item(client, credentials, category_id, data)

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}