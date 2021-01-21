import pytest

from tests.helpers import create_headers


def test_current_user_success(client, access_token):
    response = client.get("/users/me", headers=create_headers(access_token))
    json_response = response.get_json()

    assert response.status_code == 200, "Successful call should return 200 status code"
    assert json_response["id"]


def test_current_user_invalid_token(client):
    response = client.get("/users/me", headers=create_headers("aaaaa"))
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credentials call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}

