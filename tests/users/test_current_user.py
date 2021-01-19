import pytest

from tests.helpers import signin


def test_current_user_success(client):
    credentials = {"username": "hizen2501", "password": "0123456"}
    _, signin_response = signin(client, credentials)
    access_token = signin_response["access_token"]

    response = client.get("/users/me", headers={"Authorization": "Bearer {}".format(access_token)})
    json_response = response.get_json()

    assert response.status_code == 200, "Successful call should return 200 status code"
    assert json_response["id"]


@pytest.mark.parametrize("access_token", ["", "aaaaa"])
def test_current_user_invalid_token(client, access_token):
    response = client.get("/users/me", headers={"Authorization": "Bearer {}".format(access_token)})
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credentials call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}

