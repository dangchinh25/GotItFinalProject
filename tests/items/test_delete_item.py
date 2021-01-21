import pytest

from tests.helpers import create_headers, signin


def delete_item(client, access_token, item_id):
    response = client.delete(f"/items/{item_id}", headers=create_headers(access_token))

    return response


def test_delete_item_success(client, access_token):
    response = delete_item(client, access_token, item_id=5)

    assert response.status_code == 200


def test_delete_item_invalid_token(client):
    response = client.delete("/items/1")
    json_response = response.get_json()

    assert response.status_code == 400, "Missing credential call should return 400 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}


def test_delete_item_invalid_user(client):
    _, json_response = signin(client, {"username": "hizen2501", "password": "0123456"})
    response = delete_item(client, json_response["access_token"], item_id=1)
    json_response = response.get_json()

    assert response.status_code == 403, "Forbidden credential call should return 403 status code"
    assert json_response["message"] == "You are not allowed to edit this item."
    assert json_response["error"] == {}


def test_delete_item_not_exist(client, access_token):
    response = delete_item(client, access_token, item_id=100)
    json_response = response.get_json()

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}
