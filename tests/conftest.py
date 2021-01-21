import pytest

from main.controllers.category import get_category, get_categories, get_category_items, create_item, create_category
from main.controllers.item import get_item, update_item, delete_item
from main.controllers.user import app, signin, signup, get_current_user
from main.db import db
from tests.setup_db import generate_categories, generate_users, generate_items


@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all(app=app)
    return app.test_client()


@pytest.fixture
def categories_test():
    with app.app_context():
        categories = generate_categories()
    return categories


@pytest.fixture
def users_test():
    with app.app_context():
        users = generate_users()
    return users


@pytest.fixture
def items_test():
    with app.app_context():
        items = generate_items()
    return items


@pytest.fixture
def access_token(client, users_test):
    response = client.post("/users/signin", json=users_test[0])
    json_response = response.get_json()

    return json_response["access_token"]

