import pytest
import json

from main.schemas.category import CategorySchema
from tests.helpers import create_category, create_headers


@pytest.mark.parametrize("credentials, category_name, status_code", [({"username": "hizen2501", "password": "0123456"},"silverware", 201)])
def test_create_category_success(client, credentials, category_name, status_code):
    response, json_response = create_category(client, credentials, category_name)

    assert response.status_code == status_code, "Successful call should return 201 status code"
    assert CategorySchema().load(json_response), "All of object's data should be uniform"


@pytest.mark.parametrize("credentials, category_name, status_code", [({"username": "hizen2501", "password": "0123456"},"household", 400)])
def test_create_category_existed_name(client, credentials, category_name, status_code):
    response, json_response = create_category(client, credentials, category_name)

    assert response.status_code == status_code, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Category {name} already existed.".format(name=category_name)
    assert json_response["error"] == {}


@pytest.mark.parametrize("credentials, category_name, status_code", [({"username": "hizen2501", "password": "0123456"}, "", 400)])
def test_create_category_invalid_request_data(client, credentials, category_name, status_code):
    response, json_response = create_category(client, credentials, category_name)

    assert response.status_code == status_code, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_create_category_invalid_token(client):
    response = client.post("/categories", headers=create_headers(),
                           data=json.dumps({"name": "toilet"}))
    json_response = response.get_json()

    assert response.status_code == 401, "Invalid credential call should return 401 status code"
    assert json_response["message"] == "Access token required. Please sign in again."
    assert json_response["error"] == {}
