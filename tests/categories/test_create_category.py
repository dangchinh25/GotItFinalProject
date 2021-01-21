import pytest

from main.schemas.category import CategorySchema
from tests.helpers import create_headers


def create_category(client, access_token, category_name):
    response = client.post("/categories", headers=create_headers(access_token), json={"name": category_name})
    json_response = response.get_json()

    return response, json_response


@pytest.mark.parametrize("category_name, status_code", [("silverware", 201)])
def test_create_category_success(client, access_token, category_name, status_code):
    response, json_response = create_category(client, access_token, category_name)

    assert response.status_code == status_code, "Successful call should return 201 status code"
    assert CategorySchema().load(json_response), "All of object's data should be uniform"


def test_create_category_existed_name(client, access_token):
    existed_name = "household"
    response, json_response = create_category(client, access_token, existed_name)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == f"Category {existed_name} already existed."
    assert json_response["error"] == {}


@pytest.mark.parametrize("category_name, status_code", [("", 400)])
def test_create_category_invalid_request_data(client, access_token, category_name, status_code):
    response, json_response = create_category(client, access_token, category_name)

    assert response.status_code == status_code, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_create_category_missing_token(client):
    response = client.post("/categories", json={"name": "toilet"})
    json_response = response.get_json()

    assert response.status_code == 400, "Missing credential call should return 400 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}

