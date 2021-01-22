import pytest


from tests.helpers import create_authorizaton_headers
from main.schemas.item import ItemSchema
from tests.setup_db import generate_items, generate_categories


def create_item(client, category_id, data, access_token=None):
    response = client.post(f"/categories/{category_id}/items", headers=create_authorizaton_headers(access_token), json=data)
    json_response = response.get_json()

    return response, json_response


def test_create_item_successfully(client, access_token):
    categories = generate_categories()
    category_id = categories[0]["id"]
    new_item = {"name": "table", "description": "A table", "category_id": category_id}

    response, json_response = create_item(client, access_token=access_token, category_id=category_id, data=new_item)

    assert response.status_code == 201, "Successful create item should return 201"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


def test_create_item_fail_with_existed_item(client, access_token):
    categories = generate_categories()
    items = generate_items()

    category_id = categories[0]["id"]
    existed_name = items[0]["name"]
    new_item = {"name": existed_name, "description": "A table", "category_id": category_id}

    response, json_response = create_item(client, access_token=access_token, category_id=category_id, data=new_item)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Item lamp already existed."
    assert json_response["error"] == {}


@pytest.mark.parametrize("category_id, data", [
    (1, {"description": "A table", "category_id": 1}),  # Missing name
    (1, {"name": "table", "category_id": 1}),   # Missing description
    (1, {"name": "table", "description": "A table"}),  # Missing category_id
    (1, {"name": 123123123, "description": "A table", "category_id": 1}),  # Name is not string
    (1, {"name": "table", "description": 213123123, "category_id": 1}),  # Description is not string
    (1, {"name": "table", "description": "A table", "category_id": "ewewf"})  # Category_id is not int
])
def test_create_item_fail_with_invalid_request_data(client, access_token, category_id, data):
    generate_categories()

    response, json_response = create_item(client, access_token=access_token, category_id=category_id, data=data)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_create_item_fail_with_invalid_token(client):
    categories = generate_categories()
    category_id = categories[0]["id"]
    data = {"name": "table", "description": "A table", "category_id": category_id}

    response, json_response = create_item(client, category_id=category_id, data=data)

    assert response.status_code == 400, "Missing credentials call should return 400 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}


def test_create_item_fail_with_not_exist_category(client, access_token):
    generate_categories()
    not_existed_category_id = 100
    new_item = {"name": "table", "description": "A table", "category_id": not_existed_category_id}

    response, json_response = create_item(client, access_token=access_token, category_id=not_existed_category_id, data=new_item)

    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}