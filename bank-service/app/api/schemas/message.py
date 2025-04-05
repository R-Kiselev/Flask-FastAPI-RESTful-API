from marshmallow import Schema, fields


class MessageSchema(Schema):
    user_id = fields.Integer(required=True)
    date = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S')
    message = fields.String(required=True)
    data = fields.Dict(required=True)