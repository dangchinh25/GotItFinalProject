import pytest

from main.schemas.item import ItemSchema
from tests.helpers import put_item


@pytest.mark.parametrize("credentials, item_id, data", [(
        {"username": "hizen", "password": "123456"},
        1,
        {"name": "lamp2", "description": "Slightly better lamp", "category_id": 1})])
def test_put_item_success(client, credentials, item_id, data):
    response, json_response = put_item(client, credentials, item_id, data)

    assert response.status_code == 201, "Successful call should return 201 status code"
    assert ItemSchema().load(json_response), "All of object's data should be uniform"




