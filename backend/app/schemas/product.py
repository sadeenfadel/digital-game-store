from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True, allow_none=True)
    price = fields.Str(dump_only=True)
    location = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)


class PaginationSchema(Schema):
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    total = fields.Int(required=True)
    pages = fields.Int(required=True)


class ProductListResponseSchema(Schema):
    items = fields.List(fields.Nested(ProductSchema), required=True)
    pagination = fields.Nested(PaginationSchema, required=True)
