from tests.helpers import create_headers
from tests.setup_db import generate_users


def test_current_user_success(client, access_token):
    response = client.get("/users/me", headers=create_headers(access_token))
    json_response = response.get_json()

    assert response.status_code == 200, "Successful call should return 200 status code"
    assert json_response["id"]


def test_current_user_invalid_token(client):
    generate_users()
    response = client.get("/users/me", headers=create_headers("aaaaa"))
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credentials call should return 401 status code"
    assert json_response["message"] == "Invalid token. Please sign in again."
    assert json_response["error"] == {}


def test_current_user_invalid_token(client):
    generate_users()
    response = client.get("/users/me")
    json_response = response.get_json()

    assert response.status_code == 400, "Invalid credentials call should return 400 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}

