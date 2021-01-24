import pytest

from main.db import db
from main.helpers import generate_token
from main.controllers.category import get_category, get_categories, get_category_items, create_item, create_category
from main.controllers.item import get_item, update_item, delete_item
from main.controllers.user import app, signin, signup, get_current_user
from tests.setup_db import generate_users


@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all(app=app)
    return app.test_client()

