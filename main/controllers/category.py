from flask import request

from main.app import app
from main.db import db
from main.models.category import CategoryModel


@app.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    return data
