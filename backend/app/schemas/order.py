from marshmallow import Schema, fields


class CreateOrderSchema(Schema):
    product_id = fields.Int(required=True)


class OrderResponseSchema(Schema):
    id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    product_title = fields.Str(required=True)
    price = fields.Str(required=True)
    location = fields.Str(required=True)
    created_at = fields.Str(required=True)


class OrderDetailSchema(Schema):
    id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    product_title = fields.Str(required=True)
    price_at_purchase = fields.Str(required=True)
    product_location = fields.Str(required=True)
    created_at = fields.Str(required=True)
    user_id = fields.Int(required=True)


class OrderPaginationSchema(Schema):
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    total = fields.Int(required=True)
    pages = fields.Int(required=True)


class OrderListResponseSchema(Schema):
    items = fields.List(fields.Nested(OrderDetailSchema), required=True)
    pagination = fields.Nested(OrderPaginationSchema, required=True)
