from main.schemas.item import ItemSchema

from tests.setup_db import generate_users, generate_categories, generate_items


def test_get_item_success(client):
    generate_users()
    generate_categories()
    items = generate_items()
    item_id = items[0]["id"]
    response = client.get(f"/items/{item_id}")
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


def test_get_item_fail(client):
    response = client.get("/items/100")
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}


