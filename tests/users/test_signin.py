import pytest

from tests.helpers import signin


@pytest.mark.parametrize("credentials, status_code", [({"username": "hizen2501", "password": "0123456"}, 200)])
def test_signin_success(client, credentials, status_code):
    response, json_response = signin(client, credentials)

    assert response.status_code == status_code, "Successful call should return 200 status code"
    assert json_response["access_token"] is not None, "Access token should be available when signing in/up"