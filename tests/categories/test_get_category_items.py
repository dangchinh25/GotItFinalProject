import pytest

from main.schemas.item import ItemSchema
from tests.setup_db import generate_categories, generate_items, generate_users


class TestGetCategoryItems:
    def _setup(self):
        self.users = generate_users()
        self.categories = generate_categories()
        self.items = generate_items()

    def test_get_category_items_successfully(self, client):
        self._setup()

        url = create_url_with_parameters(category_id=self.categories[0]["id"], limit=10, offset=0)
        response = client.get(url)
        json_response = response.get_json()
        assert response.status_code == 200, "Successful call should return 200 status code"
        assert ItemSchema(many=True).load(json_response["items"]), "All of object's data should be uniform"

    def test_get_category_items_fail_with_not_existed_category_id(self, client):
        self._setup()
        url = create_url_with_parameters(category_id=100, limit=10, offset=0)
        response = client.get(url)
        json_response = response.get_json()
        assert response.status_code == 404, "Not found error should return 404 status code"
        assert json_response["message"] == "Category with id 100 does not exist."
        assert json_response["error"] == {}

    @pytest.mark.parametrize("limit, offset",
                             [
                                 ("a", 1),  # Limit is not int
                                 (1, "a"),  # Offset is not int
                                 ("a", "a")  # Both limit and offset is not int
                             ])
    def test_get_category_items_fail_with_invalid_request_data(self, client, limit, offset):
        self._setup()
        url = create_url_with_parameters(self.categories[0]["id"], limit=limit, offset=offset)
        response = client.get(url)
        json_response = response.get_json()
        assert response.status_code == 400, "Invalid request call should return 400 status code"
        assert json_response["message"] == "Invalid request data."
        assert json_response["error"] != {}, "Invalid request data should contain error body"

    @pytest.mark.parametrize("limit, offset",
                             [
                                 (None, 1),  # Limit is not provided
                                 (1, None),  # Offset is not provided
                                 (None, None)  # Both limit and offset is not provided
                             ])
    def test_get_category_item_fail_with_missing_data(self, client, limit, offset):
        self._setup()
        url = create_url_with_parameters(self.categories[0]["id"], limit=limit, offset=offset)
        response = client.get(url)
        assert response.status_code == 200, "Successful call should return 200 status code"


def create_url_with_parameters(category_id, limit, offset):
    if limit is None and offset is None:
        return f"/categories/{category_id}/items"
    if limit is None:
        return f"/categories/{category_id}/items?offset={offset}"
    if offset is None:
        return f"/categories/{category_id}/items?limit={limit}"
    return f"/categories/{category_id}/items?limit={limit}&offset={offset}"

