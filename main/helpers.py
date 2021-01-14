import functools
from flask import request
from marshmallow import ValidationError

from main.exceptions import InvalidRequestError

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

