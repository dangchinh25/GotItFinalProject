from flask import request, jsonify

from main.app import app
from main.db import db
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.helpers import validate_input, validate_token, check_item_exist
from main.exceptions import ForbiddenError, InternalServerError


@app.route("/items/<int:item_id>", methods=["GET"])
@check_item_exist
def get_item(item):
    return jsonify(ItemSchema().dump(item))


@app.route("/items/<int:item_id>", methods=["PUT"])
@validate_token
@validate_input(ItemSchema)
@check_item_exist
def update_item(user_id, data, item):
    if item.id != user_id:
        raise ForbiddenError()

    try:
        item.name = data["name"]
        item.description = data["description"]
        item.category_id = data["category_id"]

        db.session.add(item)
        db.session.commit()
    except Exception as e:
        raise InternalServerError()

    return jsonify(ItemSchema().dump(item))


@app.route("/items/<int:item_id>", methods=["DELETE"])
@validate_token
@check_item_exist
def delete_item(user_id, item):
    if user_id != item.id:
        raise ForbiddenError()

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        raise InternalServerError()

    return jsonify({}), 200
