from main.db import db
from main.models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "category"
    name = db.Column(db.String(20), unique=True, nullable=False)
    items = db.relationship("ItemModel", lazy="dynamic")
