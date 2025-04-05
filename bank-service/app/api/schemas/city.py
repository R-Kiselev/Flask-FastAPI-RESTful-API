from marshmallow import Schema, fields
from marshmallow import validates, ValidationError

from app.commons.validation_utils import validate_name


class CitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    @validates("name")
    def validate_name(self, value):
        validate_name(value)
