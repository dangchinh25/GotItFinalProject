from main.helpers import generate_token
from main.schemas.item import ItemSchema

from tests.setup_db import generate_users, generate_categories, generate_items


class TestGetItem:
    def _setup(self):
        self.users = generate_users()
        self.categories = generate_categories()
        self.items = generate_items()
        self.access_token = generate_token(self.users[0]["id"])

    def test_get_item_successfully(self, client):
        self._setup()

        item_id = self.items[0]["id"]
        response = client.get(f"/items/{item_id}")
        json_response = response.get_json()
        assert response.status_code == 200, "Successful call should return 200 status code"
        assert ItemSchema().load(json_response), "All of object's data should be uniform"

    def test_get_item_fail_with_not_exist_item(self, client):
        response = client.get("/items/100")
        json_response = response.get_json()
        assert response.status_code == 404, "Not found error should return 404 status code"
        assert json_response["message"] == "Item with id 100 does not exist."
        assert json_response["error"] == {}




