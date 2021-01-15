from main.schemas.category import CategorySchema


def test_get_categories(client):
    response = client.get("/categories")
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(response.get_json()) == 3, "There are 3 categories in db, get_categories should return 3 object"
    assert CategorySchema(many=True).load(response.get_json()), "All of object's data should be uniform"