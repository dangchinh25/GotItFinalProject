import pytest
import os

from main.controllers.category import *
from main.controllers.item import *
from main.controllers.user import *
from tests.setup_db import drop_table, generate_categories


@pytest.fixture
def setup():
    try:
        drop_table()
    except:
        pass
    db.create_all(app=app)
    with app.app_context():
        generate_categories()
    return app


@pytest.fixture
def client(setup):
    return setup.test_client()


