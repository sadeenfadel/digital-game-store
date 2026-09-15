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
