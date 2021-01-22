import pytest

from tests.helpers import create_headers, signin
from tests.setup_db import generate_categories, generate_items, generate_users


def delete_item(client, item_id, access_token=None):
    response = client.delete(f"/items/{item_id}", headers=create_headers(access_token))

    return response


def test_delete_item_success(client, access_token):
    generate_categories()
    items = generate_items()
    response = delete_item(client, item_id=items[0]["id"], access_token=access_token)

    assert response.status_code == 200


def test_delete_item_invalid_token(client):
    response = delete_item(client, item_id=1)
    json_response = response.get_json()

    assert response.status_code == 400, "Missing credential call should return 400 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}


def test_delete_item_invalid_user(client):
    users = generate_users()
    generate_categories()
    items = generate_items()
    _, json_response = signin(client, credentials=users[1])
    response = delete_item(client, item_id=items[0]["id"], access_token=json_response["access_token"])
    json_response = response.get_json()

    assert response.status_code == 403, "Forbidden credential call should return 403 status code"
    assert json_response["message"] == "You are not allowed to edit this item."
    assert json_response["error"] == {}


def test_delete_item_not_exist(client, access_token):
    response = delete_item(client, item_id=100, access_token=access_token)
    json_response = response.get_json()

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}
