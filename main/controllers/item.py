from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from main.app import app
from main.db import db
from main.exceptions import ForbiddenError
from main.helpers import validate_input, validate_token, check_item_exist
from main.schemas.item import ItemSchema


@app.route("/items/<int:item_id>", methods=["GET"])
@check_item_exist
def get_item(item):
    return jsonify(ItemSchema().dump(item)), 200


@app.route("/items/<int:item_id>", methods=["PUT"])
@validate_token
@validate_input(ItemSchema)
@check_item_exist
def update_item(user_id, data, item):
    if item.user_id != user_id:
        raise ForbiddenError("You are not allowed to edit this item.")

    try:
        item.name = data["name"]
        item.description = data["description"]
        item.category_id = data["category_id"]

        db.session.add(item)
        db.session.commit()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)

    return jsonify(ItemSchema().dump(item)), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
@validate_token
@check_item_exist
def delete_item(user_id, item):
    if user_id != item.user_id:
        raise ForbiddenError("You are not allowed to edit this item.")

    try:
        db.session.delete(item)
        db.session.commit()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)

    return jsonify({}), 200
