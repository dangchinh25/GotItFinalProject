from main.db import db
from main.models.user import UserModel
from main.models.category import CategoryModel
from main.models.base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = "item"
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(CategoryModel.id))
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))