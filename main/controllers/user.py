from flask import request, jsonify

from main.app import app
from main.db import db
from main.models.user import UserModel
from main.schemas.user import Schema


@app.route("/users/signin", methods=["POST"])
def signin():
    data = request.get_json()

    return jsonify(data)


@app.route("/user/signup", methods=["POST"])
def signup():
    data = request.get_json()

    return jsonify(data)


@app.route("/user/me", methods=["POST"])
def get_current_user():
    pass