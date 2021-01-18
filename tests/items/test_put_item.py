import pytest
import json

from main.schemas.item import ItemSchema
from tests.helpers import put_item, create_headers


@pytest.mark.parametrize("credentials, item_id, data", [(
        {"username": "hizen", "password": "123456"},
        1,
        {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})])
def test_put_item_success(client, credentials, item_id, data):
    response, json_response = put_item(client, credentials, item_id, data)

    assert response.status_code == 201, "Successful call should return 201 status code"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


@pytest.mark.parametrize("credentials, item_id, data", [
    ({"username": "hizen", "password": "123456"}, 1, {"description": "Slightly better lamp", "category_id": 1}),
    ({"username": "hizen", "password": "123456"}, 1, {"name": "lamp2", "category_id": 1}),
    ({"username": "hizen", "password": "123456"}, 1, {"name": "lamp2", "description": "Slightly better lamp"}),
    ({"username": "hizen", "password": "123456"}, 1, {"name": 1231232, "description": "Slightly better lamp", "category_id": 1}),
    ({"username": "hizen", "password": "123456"}, 1, {"name": "lamp2", "description": 123123, "category_id": 1}),
    ({"username": "hizen", "password": "123456"}, 1, {"name": "lamp2", 'a'*100: "Slightly better lamp", "category_id": "efwef"}),
])
def test_put_item_invalid_request_data(client, credentials, item_id, data):
    response, json_response = put_item(client, credentials=credentials, item_id=item_id, data=data)

    assert response.status_code == 400, "Invalid request data should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_put_item_invalid_token(client):
    response = client.put("/items/1",
                          headers=create_headers(),
                          data=json.dumps({"name": "lamp2", "description": "Slightly better lamp", "category_id": 1}))
    json_response = response.get_json()

    assert response.status_code == 400, "Invalid credential call should return 400 status code"
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


@pytest.mark.parametrize("credentials, item_id, data", [(
        {"username": "hizen", "password": "123456"},
        100,
        {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})])
def test_put_item_not_exist(client, credentials, item_id, data):
    response, json_response = put_item(client, credentials, item_id, data)

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}




