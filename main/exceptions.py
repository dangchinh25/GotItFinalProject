from flask import jsonify


class BaseError(Exception):
    def __init__(self):
        self.message = None
        self.status_code = None

    def messages(self):
        return jsonify({'message': self.message}), self.status_code


class InvalidRequestError(BaseError):
    def __init__(self, error):
        self.status_code = 400
        self.message = "Invalid request data."
        self.error = error


class UnauthorizedError(BaseError):
    status_code = 401


class ForbiddenError(BaseError):
    status_code = 403


class NotFoundError(BaseError):
    status_code = 404