import pytest

from main.schemas.item import ItemSchema
from tests.helpers import create_headers, signin
from tests.setup_db import generate_users, generate_items, generate_categories


def put_item(client, item_id, data, access_token=None):
    response = client.put(f"/items/{item_id}", headers=create_headers(access_token), json=data)
    json_response = response.get_json()

    return response, json_response


def test_put_item_success(client, access_token):
    categories = generate_categories()
    items = generate_items()
    data = {"name": "lamp2", "description": "Slightly better lamp", "category_id": categories[0]["id"]}
    response, json_response = put_item(client, item_id=items[0]["id"], data=data, access_token=access_token)

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
    generate_categories()
    items = generate_items()
    response, json_response = put_item(client, item_id=items[0]["id"], data=data, access_token=access_token)

    assert response.status_code == 400, "Invalid request data should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_put_item_invalid_token(client):
    data = {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1}
    response, json_response = put_item(client, item_id=1, data=data)

    assert response.status_code == 400, "Invalid credential call should return 401 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}


def test_put_item_invalid_user(client):
    generate_categories()
    users = generate_users()
    items = generate_items()
    data = {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1}
    _, json_response = signin(client, users[1])
    response, json_response = put_item(client, item_id=items[0]["id"], data=data, access_token=json_response["access_token"])

    assert response.status_code == 403, "Forbiden call should return 403 status code"
    assert json_response["message"] == "You are not allowed to edit this item."
    assert json_response["error"] == {}


def test_put_item_not_exist(client, access_token):
    data = {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1}
    response, json_response = put_item(client, item_id=100, data=data, access_token=access_token)

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}




