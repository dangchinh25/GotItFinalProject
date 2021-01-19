import functools
import jwt
from datetime import datetime, timedelta
from flask import request
from marshmallow import ValidationError
import bcrypt

from main.exceptions import BadRequestError, InternalServerError, NotFoundError, UnauthorizedError
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.pagination import PaginationSchema

from main.app import app


# load request body into json and validate according to predefined schema
def validate_input(schema):
    def wrapper(func):
        @functools.wraps(func)
        def validate(*args, **kwargs):
            try:
                data = schema().load(request.get_json())
            except ValidationError as e:
                raise BadRequestError("Invalid request data.", e.normalized_messages())

            return func(data=data, *args, **kwargs)
        return validate
    return wrapper


def check_category_exist(func):
    @functools.wraps(func)
    def check(*args, **kwargs):
        try:
            category_id = kwargs.pop("category_id")
            category = CategoryModel.query.get(category_id)
        except Exception as e:
            raise InternalServerError()
        if not category:
            raise NotFoundError("Category with id {category_id} does not exist.".format(category_id=category_id))
        return func(category=category, *args, **kwargs)
    return check


def check_item_exist(func):
    @functools.wraps(func)
    def check(*args, **kwargs):
        try:
            item_id = kwargs.pop("item_id")
            item = ItemModel.query.get(item_id)
        except Exception as e:
            raise InternalServerError()
        if not item:
            raise NotFoundError("Item with id {item_id} does not exist.".format(item_id=item_id))
        return func(item=item, *args, **kwargs)
    return check


def validate_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers["Authorization"].split()[1]
            data = jwt.decode(access_token, app.config["SECRET"], algorithms="HS256")
            user_id = data["user_id"]
        except Exception as e:
            raise UnauthorizedError("Access token required. Please sign in again.")

        return func(user_id=user_id, *args, **kwargs)

    return wrapper


def validate_pagination(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            offset = request.args.get("offset")
            limit = request.args.get("limit")
        except Exception as e:
            pass
        if not request.args.get("offset"):
            offset = 0
        if not request.args.get("limit"):
            limit = 10
        try:
            PaginationSchema().load({"limit": limit, "offset": offset})
        except ValidationError as e:
            raise BadRequestError("Invalid request data.", e.normalized_messages())

        pagination = PaginationSchema().dump({"limit": limit, "offset": offset})

        return func(pagination=pagination, *args, **kwargs)
    return wrapper


def generate_token(user_id):
    return jwt.encode({"user_id": user_id, "exp": datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET"], algorithm="HS256")


def generate_hashed_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def validate_hashed_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

