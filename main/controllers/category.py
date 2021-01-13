from flask import request

from main.app import app
from main.db import db
from main.models.category import CategoryModel

from main.schemas.category import CategorySchema
from marshmallow import ValidationError


@app.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    try:
        CategorySchema().load(data)
    except Exception as e:
        raise e

    return data


