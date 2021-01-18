import pytest

from tests.helpers import signup


@pytest.mark.parametrize("credentials, status_code", [({"username": "hizen2502", "password": "0123456"}, 201)])
def test_signup_success(client, credentials, status_code):
    response, json_response = signup(client, credentials)

    assert response.status_code == status_code, "Successful call should return 200 status code"
    assert json_response["access_token"] is not None, "Access token should be available when signing in/up"


@pytest.mark.parametrize("credentials, status_code, message", [({"username": "hizen2501", "password": "0123456789"}, 400, "Username already existed.")])
def test_signup_fail_with_existed_username(client, credentials, status_code, message):
    response, json_response = signup(client, credentials)

    assert response.status_code == status_code, "Invalid credential call should return 400 status code"
    assert json_response["message"] == message
    assert json_response["error"] == {},"Invalid credentials should not contain error body"


@pytest.mark.parametrize("credentials, status_code, message",
                         [
                             ({"username": "hizen2502"}, 400, "Invalid request data."),
                             ({"password": "0123456789"}, 400, "Invalid request data."),
                             ({"username": "", "password": "0123456789"}, 400, "Invalid request data."),
                             ({"username": "hizen2502", "password": ""}, 400, "Invalid request data."),
                         ]
                         )
def test_signup_fail_with_invalid_request_data(client, credentials, status_code, message):
    response, json_response = signup(client, credentials)

    assert response.status_code == status_code, "Invalid credential call should return 400 status code"
    assert json_response["message"] == message
    assert json_response["error"] != {}, "Invalid request data should contain error body"