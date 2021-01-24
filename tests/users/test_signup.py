import pytest

from tests.helpers import signup
from tests.setup_db import generate_users


class TestSignUp:
    def _setup(self):
        self.users = generate_users()

    def test_signup_successfully(self, client):
        credentials = {"username": "hizen2502", "password": "0123456"}
        response, json_response = signup(client, credentials=credentials)

        assert response.status_code == 201, "Successful call should return 200 status code"
        assert json_response["access_token"] is not None, "Access token should be available when signing in/up"

    def test_signup_fail_with_existed_username(self, client):
        self._setup()
        credentials = {"username": self.users[0]["username"], "password": "123456"}
        response, json_response = signup(client, credentials=credentials)

        assert response.status_code == 400, "Invalid credential call should return 400 status code"
        assert json_response["message"] == "Username already existed."
        assert json_response["error"] == {}, "Invalid credentials should not contain error body"

    @pytest.mark.parametrize("credentials",
                             [
                                 {"username": "hizen2502"},  # Missing password
                                 {"password": "0123456789"},  # Missing username
                                 {"username": "", "password": "0123456789"},  # Invalid username
                                 {"username": "hizen2502", "password": ""},  # Invalid password
                             ]
                             )
    def test_signup_fail_with_invalid_request_data(self, client, credentials):
        response, json_response = signup(client, credentials=credentials)

        assert response.status_code == 400, "Invalid credential call should return 400 status code"
        assert json_response["message"] == "Invalid request data."
        assert json_response["error"] != {}, "Invalid request data should contain error body"
