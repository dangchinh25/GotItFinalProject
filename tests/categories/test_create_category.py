from main.schemas.category import CategorySchema
from tests.helpers import create_headers
from tests.setup_db import generate_categories


new_category_name = "silverware"


def create_category(client, category_name, access_token=None):
    response = client.post("/categories", headers=create_headers(access_token), json={"name": category_name})
    json_response = response.get_json()

    return response, json_response


def test_create_category_success(client, access_token):
    generate_categories()
    response, json_response = create_category(client, access_token=access_token, category_name=new_category_name)

    assert response.status_code == 201, "Successful call should return 201 status code"
    assert CategorySchema().load(json_response), "All of object's data should be uniform"


def test_create_category_existed_name(client, access_token):
    categories = generate_categories()
    existed_name = categories[0]["name"]
    response, json_response = create_category(client, access_token=access_token, category_name=existed_name)

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == f"Category {existed_name} already existed."
    assert json_response["error"] == {}


def test_create_category_invalid_request_data(client, access_token):
    response, json_response = create_category(client, access_token=access_token, category_name="")

    assert response.status_code == 400, "Invalid request call should return 400 status code"
    assert json_response["message"] == "Invalid request data."
    assert json_response["error"] != {}


def test_create_category_missing_token(client):
    response, json_response = create_category(client, category_name=new_category_name)

    assert response.status_code == 400, "Missing credential call should return 400 status code"
    assert json_response["message"] == "Missing token. Please sign in first to perform this action."
    assert json_response["error"] == {}

