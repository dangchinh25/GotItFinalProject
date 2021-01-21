import pytest
from main.schemas.item import ItemSchema


def create_url_with_paramenters(category_id, limit, offset):
    return f"/categories/{category_id}/items?limit={limit}&offset={offset}"


def get_category_items_success(client):
    url = create_url_with_paramenters(category_id=3, limit=10, offset=0)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(json_response) == 3, "There are 3 items in db, should return 3 object"
    assert ItemSchema(many=True).load(json_response), "All of object's data should be uniform"


def test_get_category_items_nonexisted_category_id(client):
    url = create_url_with_paramenters(category_id=100, limit=10, offset=0)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}


@pytest.mark.parametrize("category_id, limit, offset", [(3, "a", 1), (3, 1, "a"), (3, "a", "a")])
def test_get_category_items_invalid_request_data(client, category_id, limit, offset):
    url = create_url_with_paramenters(category_id, limit, offset)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}, "Invalid request data should contain error body"


@pytest.mark.parametrize("url", ["/categories/3/items?offset=1", "/categories/3/items?limit=1", "/categories/3/items"])
def test_get_category_item_missing_data(client, url):
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"