class BaseError(Exception):
    status_code = None
    message = None
    error = {}

    def __init__(self, message, error=None):
        super().__init__()
        self.message = message
        if error is not None:
            self.error = error


class BadRequestError(BaseError):
    status_code = 400


class UnauthorizedError(BaseError):
    status_code = 401


class ForbiddenError(BaseError):
    status_code = 403


class NotFoundError(BaseError):
    status_code = 404


class InternalServerError(BaseError):
    status_code = 500

    def __init__(self):
        self.message = "Internal server error"


