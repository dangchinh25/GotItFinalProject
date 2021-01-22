from main.app import app
from main.db import db
from main.models.item import ItemModel
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.schemas.category import CategorySchema
from main.schemas.user import UserSchema
from main.schemas.item import ItemSchema
from main.helpers import generate_hashed_password


def generate_categories():
    categories = [
        CategoryModel(name="household"),
        CategoryModel(name="groceries"),
        CategoryModel(name="tech")
    ]
    with app.app_context():
        db.session.add_all(categories)
        db.session.commit()
        return CategorySchema(many=True).dump(categories)


def generate_users():
    users = [{"id": 1, "username": "hizen", "password": "123456"}, {"id": 2, "username": "hizen2501", "password": "0123456"}]
    with app.app_context():
        for user in users:
            new_user = UserModel(username=user["username"], password=generate_hashed_password(user["password"]))
            db.session.add(new_user)
            db.session.commit()
    return UserSchema(many=True).dump(users)


def generate_items():
    items = [
        ItemModel(user_id=1, category_id=1, name="lamp", description="This is a lamp, it emit light"),
        ItemModel(user_id=1, category_id=3, name="macbookpro", description="Expensive shit"),
        ItemModel(user_id=1, category_id=3, name="dellxps15", description="Less Expensive shit"),
        ItemModel(user_id=1, category_id=3, name="dellmonitor", description="Good stuff"),
        ItemModel(user_id=2, category_id=2, name="toiletpaper", description="We all need this"),
    ]
    with app.app_context():
        db.session.add_all(items)
        db.session.commit()
        return ItemSchema(many=True).dump(items)