from marshmallow import Schema, fields
from marshmallow.validate import Length


class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(min=1, max=20, error="Name must be between 1 and 20 characters."))
    description = fields.Str(required=True, error="You must provide description.")
    category_id = fields.Int()
    user_id = fields.Int()
    created = fields.DateTime()