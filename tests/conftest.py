import pytest
import os

from main.controllers.category import app, get_category, get_categories, get_category_items, create_item, create_category
from main.controllers.item import app, get_item, update_item, delete_item
from main.controllers.user import app, signin, signup, get_current_user
from main.db import db
from tests.setup_db import drop_table, generate_categories, generate_users, generate_items


@pytest.fixture
def setup():
    try:
        drop_table()
    except:
        pass
    db.create_all(app=app)
    with app.app_context():
        generate_categories()
        generate_users()
        generate_items()
    return app


@pytest.fixture
def client(setup):
    return setup.test_client()


