from flask import request, jsonify

from main.app import app
from main.db import db
from main.models.category import CategoryModel

from main.schemas.category import CategorySchema
from main.helpers import validate_input, check_category_exist
from main.exceptions import InternalServerError, NotFoundError


@app.route("/categories", methods=["GET"])
def get_categories():
    # get all categories
    try:
        categories = CategoryModel.query.all()
    except Exception as e:
        raise InternalServerError()
    
    return jsonify(CategorySchema(many=True).dump(categories))


@app.route("/categories/<int:category_id>", methods=["GET"])
@check_category_exist
def get_category(category):
    # get info of 1 category
    return jsonify(CategorySchema().dump(category))


@app.route("/categories/<int:category_id>/items", methods=["GET"])
def get_category_items(category_id):
    # get all items of a particular category
    req = request.args.get("limit")

    return jsonify(req)


@app.route("/categories", methods=["POST"])
@validate_input(CategorySchema)
def create_category(data):
    # create new category
    new_category = CategoryModel(name=data["name"])
    try:
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        raise InternalServerError()

    return jsonify(CategorySchema().dump(new_category)), 201

