from main.helpers import generate_token
from main.schemas.category import CategorySchema
from tests.helpers import create_authorizaton_headers
from tests.setup_db import generate_categories, generate_users


class TestCreateCategory:
    new_category_name = "silverware"

    def _setup(self):
        self.users = generate_users()
        self.categories = generate_categories()
        self.access_token = generate_token(self.users[0]["id"])

    def test_create_category_successfully(self, client):
        self._setup()
        response, json_response = create_category(client, access_token=self.access_token,
                                                  category_name=self.new_category_name)

        assert response.status_code == 201, "Successful call should return 201 status code"
        assert CategorySchema().load(json_response), "All of object's data should be uniform"

    def test_create_category_fail_with_existed_name(self, client):
        self._setup()
        existed_name = self.categories[0]["name"]
        response, json_response = create_category(client, access_token=self.access_token, category_name=existed_name)

        assert response.status_code == 400, "Invalid request call should return 400 status code"
        assert json_response["message"] == f"Category {existed_name} already existed."
        assert json_response["error"] == {}

    def test_create_category_fail_with_invalid_request_data(self, client):
        self._setup()
        response, json_response = create_category(client, access_token=self.access_token, category_name="")

        assert response.status_code == 400, "Invalid request call should return 400 status code"
        assert json_response["message"] == "Invalid request data."
        assert json_response["error"] != {}

    def test_create_category_fail_with_missing_token(self, client):
        response, json_response = create_category(client, category_name=self.new_category_name)

        assert response.status_code == 400, "Missing credential call should return 400 status code"
        assert json_response["message"] == "Missing token. Please sign in first to perform this action."
        assert json_response["error"] == {}


def create_category(client, category_name, access_token=None):
    response = client.post("/categories", headers=create_authorizaton_headers(access_token),
                           json={"name": category_name})
    json_response = response.get_json()

    return response, json_response
