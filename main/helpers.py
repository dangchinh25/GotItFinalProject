import functools
import jwt
from datetime import datetime, timedelta
from flask import request
from marshmallow import ValidationError

from main.exceptions import InvalidRequestError, InternalServerError, NotFoundError
from main.models.category import CategoryModel

from main.app import app


# load request body into json and validate according to predefined schema
def validate_input(schema):
    def wrapper(func):
        @functools.wraps(func)
        def validate(*args, **kwargs):
            try:
                data = schema().load(request.get_json())
            except ValidationError as e:
                raise e

            return func(data=data, *args, **kwargs)
        return validate
    return wrapper


def check_category_exist(func):
    @functools.wraps(func)
    def check(*args, **kwargs):
        try:
            category = CategoryModel.query.get(kwargs.pop("category_id"))
        except Exception as e:
            raise InternalServerError()
        if not category:
            raise NotFoundError()
        return func(category=category, *args, **kwargs)
    return check


def validate_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers["Authorization"].split()[1]
            data = jwt.decode(access_token, app.config["SECRET"], algorithms="HS256")
            user_id = data["user_id"]
        except Exception as e:
            print(e)
            raise InvalidRequestError()

        return func(user_id=user_id, *args, **kwargs)

    return wrapper



def generate_token(user_id):
    return jwt.encode({"user_id": user_id, "exp": datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET"], algorithm="HS256")

