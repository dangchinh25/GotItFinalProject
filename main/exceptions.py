from flask import jsonify


class BaseError(Exception):
    def __init__(self):
        self.message = None
        self.status_code = None

    def messages(self):
        return jsonify({'message': self.message}), self.status_code


class InvalidRequestError(BaseError):
    def __init__(self):
        self.status_code = 400
        self.message = "Invalid request data."


class UnauthorizedError(BaseError):
    status_code = 401


class ForbiddenError(BaseError):
    status_code = 403


class NotFoundError(BaseError):
    def __init__(self):
        self.status_code = 404
        self.message = "Not found error."


class InternalServerError(BaseError):
    def __init__(self):
        self.status_code = 500
        self.message = "Internal server error."
