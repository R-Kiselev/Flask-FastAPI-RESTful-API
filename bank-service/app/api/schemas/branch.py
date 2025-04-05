from marshmallow import Schema, fields
from marshmallow import validates, ValidationError

from app.commons.validation_utils import validate_id


class BranchSchema(Schema):
    id = fields.Int(dump_only=True)
    bank_id = fields.Int(required=True)
    city_id = fields.Int(required=True)

    @validates("bank_id")
    def validate_bank_id(self, value):
        validate_id(value)

    @validates("city_id")
    def validate_city_id(self, value):
        validate_id(value)
