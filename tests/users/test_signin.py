import pytest

from tests.helpers import signin
from tests.setup_db import generate_users


def test_signin_success(client):
    users = generate_users()
    response, json_response = signin(client, users[0])

    assert response.status_code == 200, "Successful call should return 200 status code"
    assert json_response["access_token"] is not None, "Access token should be available when signing in/up"


def test_signin_fail_with_invalid_credentials(client):
    users = generate_users()
    credentials = users[0]
    credentials["password"] = "0123456789"
    response, json_response = signin(client, credentials)

    assert response.status_code == 400, "Invalid credential call should return 400 status code"
    assert json_response["message"] == "Invalid credentials."
    assert json_response["error"] == {}, "Invalid credentials should not contain error body"


@pytest.mark.parametrize("credentials",
                         [
                             {"username": "hizen2501"},
                             {"password": "0123456789"},
                             {"username": "", "password": "0123456789"},
                             {"username": "hizen2501", "password": ""},
                         ]
                         )
def test_signin_fail_with_invalid_request_data(client, credentials):
    response, json_response = signin(client, credentials)

    assert response.status_code == 400, "Invalid credential call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}, "Invalid request data should contain error body"