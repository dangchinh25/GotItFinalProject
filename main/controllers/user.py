from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from main.app import app
from main.db import db
from main.exceptions import BadRequestError
from main.helpers import generate_token, validate_token, generate_hashed_password, validate_hashed_password, \
    validate_input
from main.models.user import UserModel
from main.schemas.user import UserSchema


@app.route("/users/signin", methods=["POST"])
@validate_input(UserSchema)
def signin(data):
    try:
        existing_user = UserModel.query.filter_by(username=data["username"]).one_or_none()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)
    if not existing_user or not validate_hashed_password(data["password"], existing_user.password):
        raise BadRequestError("Invalid credentials.")

    return jsonify({"access_token": generate_token(existing_user.id)}), 200


@app.route("/users/signup", methods=["POST"])
@validate_input(UserSchema)
def signup(data):
    try:
        existing_user = UserModel.query.filter_by(username=data["username"]).one_or_none()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)

    if existing_user:
        raise BadRequestError("Username already existed.")

    data["password"] = generate_hashed_password(data["password"])
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as error:
        raise SQLAlchemyError(error)

    return jsonify({"access_token": generate_token(user.id)}), 201


@app.route("/users/me", methods=["GET"])
@validate_token
def get_current_user(user_id):
    return jsonify({"id": user_id}), 200