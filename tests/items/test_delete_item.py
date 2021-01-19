import pytest

from tests.helpers import delete_item, create_headers


def test_delete_item_success(client):
    credentials = {"username": "hizen", "password": "123456"}
    response = delete_item(client, credentials, item_id=1)

    assert response.status_code == 200


def test_delete_item_invalid_token(client):
    response = client.delete("/items/1", headers=create_headers())
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credential call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}


def test_delete_item_invalid_user(client):
    credentials = {"username": "hizen2501", "password": "0123456"}
    response = delete_item(client, credentials, item_id=1)
    json_response = response.get_json()

    assert response.status_code == 403, "Forbidden credential call should return 403 status code"
    assert json_response["message"] == "You are not allowed to edit this item."
    assert json_response["error"] == {}


def test_delete_item_not_exist(client):
    credentials = {"username": "hizen", "password": "123456"}
    response = delete_item(client, credentials, item_id=100)
    json_response = response.get_json()

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}
