import pytest
import json

from tests.helpers import create_headers
from main.schemas.item import ItemSchema


def create_item(client, access_token, category_id, data):
    response = client.post(f"/categories/{category_id}/items", headers=create_headers(access_token), json=data)
    json_response = response.get_json()

    return response, json_response


@pytest.mark.parametrize("category_id, data", [
    (1, {"name": "table", "description": "A table", "category_id": 1})])
def test_create_item_success(client, access_token, category_id, data):
    response, json_response = create_item(client, access_token, category_id, data)

    assert response.status_code == 201, "Successful create item should return 201"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


@pytest.mark.parametrize("category_id, data", [
    (1, {"name": "lamp", "description": "A table", "category_id": 1})])
def test_create_item_existed_item(client, access_token, category_id, data):
    response, json_response = create_item(client, access_token, category_id, data)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Item lamp already existed."
    assert json_response["error"] == {}


@pytest.mark.parametrize("category_id, data", [
    (1, {"description": "A table", "category_id": 1}),
    (1, {"name": "table", "category_id": 1}),
    (1, {"name": "table", "description": "A table", }),
    (1, {"name": 123123123, "description": "A table", "category_id": 1}),
    (1, {"name": "table", "description": 213123123, "category_id": 1}),
    (1, {"name": "table", "description": "A table", "category_id": "ewewf"})
])
def test_create_invalid_request_data(client, access_token, category_id, data):
    response, json_response = create_item(client, access_token, category_id, data)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_create_item_invalid_token(client):
    response = client.post("/categories/1/items", headers=create_headers(), json={"name": "lamp", "description": "A table", "category_id": 1})
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credentials call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}


@pytest.mark.parametrize("category_id, data", [
    (100, {"name": "table", "description": "A table", "category_id": 100})])
def test_create_item_not_exist_category(client, access_token, category_id, data):
    response, json_response = create_item(client, access_token, category_id, data)

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}