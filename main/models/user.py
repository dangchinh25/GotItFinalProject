from main.db import db
from main.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    items = db.relationship("ItemModel", lazy="dynamic")
