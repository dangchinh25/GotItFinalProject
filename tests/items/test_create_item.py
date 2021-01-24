import pytest

from main.schemas.item import ItemSchema
from main.helpers import generate_token
from tests.helpers import create_authorizaton_headers
from tests.setup_db import generate_items, generate_categories, generate_users


class TestCreateItem:
    def _setup(self):
        self.users = generate_users()
        self.categories = generate_categories()
        self.items = generate_items()
        self.access_token = generate_token(self.users[0]["id"])

    def test_create_item_successfully(self, client):
        self._setup()
        category_id = self.categories[0]["id"]
        new_item = {"name": "table", "description": "A table", "category_id": category_id}

        response, json_response = create_item(client, access_token=self.access_token, category_id=category_id, data=new_item)

        assert response.status_code == 201, "Successful create item should return 201"
        assert ItemSchema().load(json_response), "All of object's data should be uniform"

    def test_create_item_fail_with_existed_item(self, client):
        self._setup()
        category_id = self.categories[0]["id"]
        existed_name = self.items[0]["name"]
        new_item = {"name": existed_name, "description": "A table", "category_id": category_id}

        response, json_response = create_item(client, access_token=self.access_token, category_id=category_id, data=new_item)

        assert response.status_code == 400, "Invalid request call should return 400 status code"
        assert json_response["message"] == "Item lamp already existed."
        assert json_response["error"] == {}

    @pytest.mark.parametrize("category_id, data", [
        (1, {"description": "A table", "category_id": 1}),  # Missing name
        (1, {"name": "table", "category_id": 1}),  # Missing description
        (1, {"name": "table", "description": "A table"}),  # Missing category_id
        (1, {"name": 123123123, "description": "A table", "category_id": 1}),  # Name is not string
        (1, {"name": "table", "description": 213123123, "category_id": 1}),  # Description is not string
        (1, {"name": "table", "description": "A table", "category_id": "ewewf"})  # Category_id is not int
    ])
    def test_create_item_fail_with_invalid_request_data(self, client, category_id, data):
        self._setup()
        response, json_response = create_item(client, access_token=self.access_token, category_id=category_id, data=data)

        assert response.status_code == 400, "Invalid request call should return 400 status code"
        assert json_response["message"] == "Invalid request data."
        assert json_response["error"] != {}

    def test_create_item_fail_with_invalid_token(self, client):
        self._setup()
        category_id = self.categories[0]["id"]
        data = {"name": "table", "description": "A table", "category_id": category_id}

        response, json_response = create_item(client, category_id=category_id, data=data)

        assert response.status_code == 400, "Missing credentials call should return 400 status code"
        assert json_response["message"] == "Missing token. Please sign in first to perform this action."
        assert json_response["error"] == {}

    def test_create_item_fail_with_not_exist_category(self, client):
        self._setup()
        not_existed_category_id = 100
        new_item = {"name": "table", "description": "A table", "category_id": not_existed_category_id}

        response, json_response = create_item(client, access_token=self.access_token, category_id=not_existed_category_id,
                                              data=new_item)

        assert response.status_code == 404, "Not found error should return 404 status code"
        assert json_response["message"] == "Category with id 100 does not exist."
        assert json_response["error"] == {}


def create_item(client, category_id, data, access_token=None):
    response = client.post(f"/categories/{category_id}/items", headers=create_authorizaton_headers(access_token), json=data)
    json_response = response.get_json()

    return response, json_response


