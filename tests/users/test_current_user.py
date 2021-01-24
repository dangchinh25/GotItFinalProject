from main.helpers import generate_token
from tests.helpers import create_authorizaton_headers
from tests.setup_db import generate_users


class TestCurrentUser:
    def _setup(self):
        self.users = generate_users()
        self.access_token = generate_token(self.users[0]["id"])

    def test_current_user_successfully(self, client):
        self._setup()
        response = client.get("/users/me", headers=create_authorizaton_headers(self.access_token))
        json_response = response.get_json()

        assert response.status_code == 200, "Successful call should return 200 status code"
        assert json_response["id"]

    def test_current_user_fail_with_invalid_token(self, client):
        response = client.get("/users/me", headers=create_authorizaton_headers("aaaaa"))
        json_response = response.get_json()

        assert response.status_code == 401, "Invalid credentials call should return 401 status code"
        assert json_response["message"] == "Invalid token. Please sign in again."
        assert json_response["error"] == {}

    def test_current_user_fail_with_missing_token(self, client):
        response = client.get("/users/me")
        json_response = response.get_json()

        assert response.status_code == 400, "Invalid credentials call should return 400 status code"
        assert json_response["message"] == "Missing token. Please sign in first to perform this action."
        assert json_response["error"] == {}
