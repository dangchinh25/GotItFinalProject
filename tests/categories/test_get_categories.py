from main.schemas.category import CategorySchema
from tests.setup_db import generate_categories


def test_get_categories(client):
    categories = generate_categories()

    response = client.get("/categories")
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert len(json_response) == len(categories)
    assert CategorySchema(many=True).load(json_response), "All of object's data should be uniform"
