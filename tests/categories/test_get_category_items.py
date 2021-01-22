import pytest
from main.schemas.item import ItemSchema
from tests.setup_db import generate_categories, generate_items


def create_url_with_parameters(category_id, limit, offset):
    if limit is None and offset is None:
        return f"/categories/{category_id}/items"
    if limit is None:
        return f"/categories/{category_id}/items?offset={offset}"
    if offset is None:
        return f"/categories/{category_id}/items?limit={limit}"
    return f"/categories/{category_id}/items?limit={limit}&offset={offset}"


def get_category_items_success(client):
    categories = generate_categories()
    generate_items()

    url = create_url_with_parameters(category_id=categories[0]["id"], limit=10, offset=0)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(json_response) == 3, "There are 3 items in db, should return 3 object"
    assert ItemSchema(many=True).load(json_response), "All of object's data should be uniform"


def test_get_category_items_nonexisted_category_id(client):
    generate_categories()
    url = create_url_with_parameters(category_id=100, limit=10, offset=0)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}


@pytest.mark.parametrize("limit, offset", [("a", 1), (1, "a"), ("a", "a")])
def test_get_category_items_invalid_request_data(client, limit, offset):
    categories = generate_categories()
    url = create_url_with_parameters(categories[0]["id"], limit, offset)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}, "Invalid request data should contain error body"


@pytest.mark.parametrize("limit, offset", [(None, 1), (1, None), (None, None)])
def test_get_category_item_missing_data(client, limit, offset):
    categories = generate_categories()
    url = create_url_with_parameters(categories[0]["id"], limit, offset)
    print(url)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"