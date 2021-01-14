from flask import request, jsonify

from main.app import app
from main.db import db


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify(item_id)


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()

    return jsonify(data)


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    pass


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    
    return jsonify(data)