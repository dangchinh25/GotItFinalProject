from flask import request, jsonify
import bcrypt

from main.app import app
from main.db import db
from main.models.user import UserModel
from main.schemas.user import UserSchema
from main.helpers import validate_input
from main.exceptions import InvalidRequestError, InternalServerError, UnauthorizedError
from main.helpers import generate_token


@app.route("/users/signin", methods=["POST"])
@validate_input(UserSchema)
def signin(data):
    try:
        existing_user = UserModel.query.filter_by(username=data["username"]).one_or_none()
    except Exception as e:
        raise InternalServerError()
    if not existing_user or not bcrypt.checkpw(data["password"].encode("utf-8"), existing_user.password.encode("utf-8")):
        raise UnauthorizedError()

    return jsonify({"access_token": generate_token(existing_user.id)}), 200


@app.route("/users/signup", methods=["POST"])
@validate_input(UserSchema)
def signup(data):
    try:
        existing_user = UserModel.query.filter_by(username=data["username"]).one_or_none()
    except Exception as e:
        raise InternalServerError()

    if existing_user:
        raise InvalidRequestError()

    data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        raise InternalServerError()

    return jsonify({"access_token": generate_token(user.id)}), 201


@app.route("/user/me", methods=["POST"])
def get_current_user():
    pass