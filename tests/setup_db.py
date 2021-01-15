from sqlalchemy import create_engine

from main.models.item import ItemModel
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.config import config
from main.db import db


def generate_categories():
    categories = [CategoryModel(name="household"), CategoryModel(name="groceries"), CategoryModel(name="tech")]
    db.session.add_all(categories)
    db.session.commit()





def drop_table():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    ItemModel.__table__.drop(engine)
    CategoryModel.__table__.drop(engine)
    UserModel.__table__.drop(engine)