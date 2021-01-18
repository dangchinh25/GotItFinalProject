from main.schemas.category import CategorySchema


def test_get_category_success(client):
    response = client.get("/categories/1")
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(response.get_json()) == 3, "There are 3 categories in db, get_categories should return 3 object"
    assert CategorySchema().load(response.get_json()), "All of object's data should be uniform"


def test_get_category_fail(client):
    response = client.get("/categories/100")
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}



