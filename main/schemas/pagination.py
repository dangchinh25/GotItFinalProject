from marshmallow import Schema, fields


class PaginationSchema(Schema):
    limit = fields.Int(error="Limit must be of type int")
    offset = fields.Int(error="Offset must be of type int.")