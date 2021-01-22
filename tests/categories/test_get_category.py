from main.schemas.category import CategorySchema
from tests.setup_db import generate_categories


def test_get_category_successfully(client):
    categories = generate_categories()
    category_id = categories[0]["id"]
    response = client.get(f"/categories/{category_id}")
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert CategorySchema().load(json_response), "All of object's data should be uniform"


def test_get_category__fail_with_not_exist_id(client):
    response = client.get("/categories/100")
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}



