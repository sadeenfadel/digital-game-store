from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginResponseSchema(Schema):
    access_token = fields.Str(required=True)
    user = fields.Dict(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(dump_only=True)
    created_at = fields.Str(dump_only=True)
