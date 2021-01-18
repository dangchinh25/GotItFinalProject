from sqlalchemy import create_engine

from main.models.item import ItemModel
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.config import config
from main.db import db
from main.helpers import generate_hashed_password


def generate_categories():
    categories = [
        CategoryModel(name="household"),
        CategoryModel(name="groceries"),
        CategoryModel(name="tech")
    ]
    db.session.add_all(categories)
    db.session.commit()


def generate_users():
    users = [
        UserModel(username="hizen", password=generate_hashed_password("123456")),
        UserModel(username="hizen2501", password=generate_hashed_password("0123456"))
    ]

    db.session.add_all(users)
    db.session.commit()


def generate_items():
    items = [
        ItemModel(user_id=1, category_id=1, name="lamp", description="This is a lamp, it emit light"),
        ItemModel(user_id=1, category_id=3, name="macbookpro", description="Expensive shit"),
        ItemModel(user_id=1, category_id=3, name="dellxps15", description="Less Expensive shit"),
        ItemModel(user_id=1, category_id=3, name="dellmonitor", description="Good stuff"),
    ]

    db.session.add_all(items)
    db.session.commit()


def drop_table():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    ItemModel.__table__.drop(engine)
    CategoryModel.__table__.drop(engine)
    UserModel.__table__.drop(engine)