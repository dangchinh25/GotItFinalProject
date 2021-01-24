from main.app import app
from main.db import db
from main.models.user import UserModel
from main.models.item import ItemModel
from main.models.category import CategoryModel


with app.app_context():
    db.create_all()