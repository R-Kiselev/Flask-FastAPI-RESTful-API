from marshmallow import Schema, fields
from marshmallow import validates

from app.commons.validation_utils import validate_name


class BankSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    @validates("name")
    def validate_name(self, value):
        validate_name(value)
