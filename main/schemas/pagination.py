from marshmallow import Schema, fields
from marshmallow.validate import Range


class PaginationSchema(Schema):
    limit = fields.Int(validate=Range(min=1, max=25, error="Limit must be greater than 1 and smaller than 25."))
    offset = fields.Int(validate=Range(min=0, error="Offset must be greater than 0."))