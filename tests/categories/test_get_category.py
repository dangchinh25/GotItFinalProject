from main.schemas.category import CategorySchema


def test_get_category_success(client):
    response = client.get("/categories/1")
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert CategorySchema().load(json_response), "All of object's data should be uniform"


def test_get_category_fail(client):
    response = client.get("/categories/100")
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Category with id 100 does not exist."
    assert json_response["error"] == {}


