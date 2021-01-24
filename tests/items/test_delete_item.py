from main.helpers import generate_token
from tests.helpers import create_authorizaton_headers
from tests.setup_db import generate_categories, generate_items, generate_users


class TestDeleteItem:
    def _setup(self):
        self.users = generate_users()
        self.categories = generate_categories()
        self.items = generate_items()
        self.access_token = generate_token(self.users[0]["id"])

    def test_delete_item_successfully(self, client):
        self._setup()
        response = delete_item(client, item_id=self.items[0]["id"], access_token=self.access_token)

        assert response.status_code == 200

    def test_delete_item_fail_with_invalid_token(self, client):
        response = delete_item(client, item_id=1)
        json_response = response.get_json()

        assert response.status_code == 400, "Missing credential call should return 400 status code"
        assert json_response["message"] == "Missing token. Please sign in first to perform this action."
        assert json_response["error"] == {}

    def test_delete_item_fail_with_invalid_user(self, client):
        self._setup()
        access_token = generate_token(self.users[1])
        response = delete_item(client, item_id=self.items[0]["id"], access_token=access_token)
        json_response = response.get_json()

        assert response.status_code == 403, "Forbidden credential call should return 403 status code"
        assert json_response["message"] == "You are not allowed to edit this item."
        assert json_response["error"] == {}

    def test_delete_item_fail_with_not_exist_item(self, client):
        self._setup()
        response = delete_item(client, item_id=100, access_token=self.access_token)
        json_response = response.get_json()

        assert response.status_code == 404, "Not found error should return 404 status code"
        assert json_response["message"] == "Item with id 100 does not exist."
        assert json_response["error"] == {}


def delete_item(client, item_id, access_token=None):
    response = client.delete(f"/items/{item_id}", headers=create_authorizaton_headers(access_token))

    return response
