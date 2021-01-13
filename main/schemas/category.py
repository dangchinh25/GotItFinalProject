from marshmallow import Schema, ValidationError, fields
from marshmallow.validate import Length


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.String(required=True, validate=Length(min=1, max=20, error="Name must be between 1 and 20 characters."))
    created = fields.DateTime(dump_only=True)