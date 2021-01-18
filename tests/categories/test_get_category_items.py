import pytest
from main.schemas.item import ItemSchema


def create_url_with_paramenters(category_id, limit, offset):
    return "/categories/{}/items?limit={}&offset={}".format(category_id, limit, offset)


def get_category_items_success(client):
    url = create_url_with_paramenters(category_id=3, limit=10, offset=0)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(json_response) == 3, "There are 3 items in db, should return 3 object"
    assert ItemSchema(many=True).load(json_response), "All of object's data should be uniform"


def test_get_category_items_with_nonexistend_category_id(client):
    url = create_url_with_paramenters(category_id=100, limit=10, offset=0)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}


@pytest.mark.parametrize("limit, offset", [("aaa", 1), (1, "aaa")])
def test_get_category_items_with_invalid_request_data(client, limit, offset):
    url = create_url_with_paramenters(category_id=1, limit=limit, offset=offset)
    response = client.get(url)
    json_response = response.get_json()
    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}, "Invalid request data should contain error body"