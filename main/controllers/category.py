from flask import request, jsonify

from main.app import app
from main.db import db
from main.models.category import CategoryModel

from main.schemas.category import CategorySchema
from marshmallow import ValidationError
from main.helpers import validate_input


@app.route("/categories", methods=["GET"])
def get_categories():
    pass


@app.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    return jsonify(category_id)


@app.route("/categories/<int:category_id>/items", methods=["GET"])
def get_category_items(category_id):
    req = request.args.get("limit")

    return jsonify(req)


@app.route("/categories", methods=["POST"])
@validate_input(CategorySchema)
def create_category(data):
    new_category = CategoryModel(name=data["name"])
    try:
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        raise e

    return jsonify(CategorySchema().dump(new_category)), 201

