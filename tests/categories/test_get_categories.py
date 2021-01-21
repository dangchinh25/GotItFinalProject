from main.schemas.category import CategorySchema


def test_get_categories(client, categories_test):
    response = client.get("/categories")
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(json_response) == len(categories_test)
    assert CategorySchema(many=True).load(json_response), "All of object's data should be uniform"
