from marshmallow import Schema, fields
from marshmallow import validates, ValidationError

from app.commons.validation_utils import validate_name, validate_id


class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    social_status_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

    @validates("name")
    def validate_name(self, value):
        validate_name(value)

    @validates("social_status_id")
    def validate_social_status_id(self, value):
        validate_id(value)

    @validates("user_id")
    def validate_user_id(self, value):
        validate_id(value)
