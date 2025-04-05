from marshmallow import Schema, fields
from marshmallow import validates

from app.commons.validation_utils import validate_balance


class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    balance = fields.Int()
    client_id = fields.Int(required=True)
    bank_id = fields.Int(required=True)

    @validates("balance")
    def validate_balance(self, value):
        validate_balance(value)
