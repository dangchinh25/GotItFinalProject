from marshmallow import Schema, fields
from marshmallow.validate import Length


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(min=1, max=20, error="Name must be between 1 and 20 characters."))
    created = fields.DateTime()