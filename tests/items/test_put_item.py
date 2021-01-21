import pytest
import json

from main.schemas.item import ItemSchema
from tests.helpers import create_headers


def put_item(client, access_token, item_id, data):
    response = client.put(f"/items/{item_id}", headers=create_headers(access_token), json=data)
    json_response = response.get_json()

    return response, json_response


@pytest.mark.parametrize("item_id, data", [(
        1,
        {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})])
def test_put_item_success(client, access_token, item_id, data):
    response, json_response = put_item(client, access_token, item_id, data)

    assert response.status_code == 201, "Successful call should return 201 status code"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


@pytest.mark.parametrize("item_id, data", [
    (1, {"description": "Slightly better lamp", "category_id": 1}),
    (1, {"name": "lamp2", "category_id": 1}),
    (1, {"name": "lamp2", "description": "Slightly better lamp"}),
    (1, {"name": 1231232, "description": "Slightly better lamp", "category_id": 1}),
    (1, {"name": "lamp2", "description": 123123, "category_id": 1}),
    (1, {"name": "lamp2", 'a'*100: "Slightly better lamp", "category_id": "efwef"}),
])
def test_put_item_invalid_request_data(client, access_token, item_id, data):
    response, json_response = put_item(client, access_token, item_id, data)

    assert response.status_code == 400, "Invalid request data should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_put_item_invalid_token(client):
    response = client.put("/items/1",
                          json={"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credential call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}


@pytest.mark.parametrize("credentials, item_id, data", [(
        {"username": "hizen2501", "password": "0123456"},
        1,
        {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})])
def test_put_item_invalid_user(client, credentials, item_id, data):
    response, json_response = put_item(client, credentials, item_id, data)

    assert response.status_code == 403, "Forbiden call should return 403 status code"
    assert json_response["message"] == "You are not allowed to edit this item."
    assert json_response["error"] == {}


@pytest.mark.parametrize("item_id, data", [(
        100,
        {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})])
def test_put_item_not_exist(client, access_token, item_id, data):
    response, json_response = put_item(client, access_token, item_id, data)

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}




