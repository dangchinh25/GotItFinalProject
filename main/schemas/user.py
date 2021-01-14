from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserSchema(Schema):
    username = fields.Str(required=True, validate=Length(min=1, max=20, error="User must be between 1 and 20 characters."))
    password = fields.Str(required=True, error="You must provide your password.")