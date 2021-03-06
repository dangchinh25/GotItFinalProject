from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from main.app import app
from main.db import db
from main.exceptions import BadRequestError
from main.helpers import validate_input, check_category_exist, validate_token, validate_pagination
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.category import CategorySchema
from main.schemas.item import ItemSchema


@app.route("/categories", methods=["GET"])
def get_categories():
    try:
        categories = CategoryModel.query.all()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)
    
    return jsonify(CategorySchema(many=True).dump(categories)), 200


@app.route("/categories/<int:category_id>", methods=["GET"])
@check_category_exist
def get_category(category):
    return jsonify(CategorySchema().dump(category)), 200


@app.route("/categories/<int:category_id>/items", methods=["GET"])
@check_category_exist
@validate_pagination
def get_category_items(category, pagination):
    try:
        items = ItemSchema(many=True).dump(category.items.limit(pagination["limit"]).offset(pagination["offset"]))
        total = category.items.count()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)

    return jsonify({"items": items, "total": total}), 200


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@validate_token
@check_category_exist
@validate_input(ItemSchema)
def create_item(user_id, category, data):
    item_name = data["name"]
    try:
        existing_item = ItemModel.query.filter_by(name=item_name).one_or_none()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)
    if existing_item:
        raise BadRequestError(f"Item {item_name} already existed.")

    new_item = ItemModel(user_id=user_id, **data)
    try:
        db.session.add(new_item)
        db.session.commit()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)
    
    return jsonify(ItemSchema().dump(new_item)), 201


@app.route("/categories", methods=["POST"])
@validate_token
@validate_input(CategorySchema)
def create_category(user_id, data):
    category_name = data["name"]
    try:
        existing_category = CategoryModel.query.filter_by(name=category_name).one_or_none()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)
    if existing_category:
        raise BadRequestError(f"Category {category_name} already existed.")
    # create new category
    new_category = CategoryModel(name=category_name)
    try:
        db.session.add(new_category)
        db.session.commit()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)

    return jsonify(CategorySchema().dump(new_category)), 201
