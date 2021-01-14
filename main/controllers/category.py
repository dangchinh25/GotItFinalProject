from flask import request, jsonify

from main.app import app
from main.db import db
from main.models.category import CategoryModel
from main.models.item import ItemModel

from main.schemas.category import CategorySchema
from main.schemas.item import ItemSchema
from main.helpers import validate_input, check_category_exist, validate_token
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
@check_category_exist
def get_category_items(category):
    # get all items of a particular category

    return jsonify({"items": ItemSchema(many=True).dump(category.items.all())}), 200


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@validate_token
@check_category_exist
@validate_input(ItemSchema)
def create_item(user_id, category, data):
    new_item = ItemModel(user_id=user_id, category_id=category.id, **data)
    try:
        db.session.add(new_item)
        db.session.commit()
    except Exception as e:
        raise InternalServerError()
    
    return jsonify(ItemSchema().dump(new_item)), 201


@app.route("/categories", methods=["POST"])
@validate_token
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


