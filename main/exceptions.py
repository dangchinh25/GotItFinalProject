from flask import jsonify


class BaseError(Exception):
    status_code = None
    message = None
    error_data = {}

    def __init__(self, message, error):
        super().__init__()
        self.message = message
        self.error_data = error


class InvalidRequestError(BaseError):
    status_code = 400


class UnauthorizedError(BaseError):
    def __init__(self):
        self.status_code = 401
        self.message = "Invalid credentials"


class ForbiddenError(BaseError):
    def __init__(self):
        self.status_code = 403
        self.message = "Unauthorized user."


class NotFoundError(BaseError):
    def __init__(self):
        self.status_code = 404
        self.message = "Not found error."


class InternalServerError(BaseError):
    def __init__(self):
        self.status_code = 500
        self.message = "Internal server error."
