from marshmallow import Schema, fields
from marshmallow import validates, ValidationError

from app.commons.validation_utils import validate_balance, validate_id


class CardSchema(Schema):
    id = fields.Int(dump_only=True)
    balance = fields.Int()
    account_id = fields.Int(required=True)

    @validates("balance")
    def validate_balance(self, value):
        validate_balance(value)

    @validates("account_id")
    def validate_account_id(self, value):
        validate_id(value)
