from main.schemas.item import ItemSchema


def test_get_item_success(client):
    response = client.get("/items/1")
    json_response = response.get_json()
    assert response.status_code == 200, "Successful call should return 200 status code"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"


def test_get_item_fail(client):
    response = client.get("/items/100")
    json_response = response.get_json()
    assert response.status_code == 404, "Not found error should return 404 status code"
    assert json_response["message"] == "Item with id 100 does not exist."
    assert json_response["error"] == {}


