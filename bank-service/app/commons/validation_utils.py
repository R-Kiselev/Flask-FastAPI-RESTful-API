import re

from marshmallow import ValidationError

def validate_balance(value):
    if value < 0:
        raise ValidationError("Balance must be a positive integer.")


def validate_id(value):
    if value <= 0:
        raise ValidationError("ID must be a positive integer.")


def validate_name(value):
    if not re.match(r"^[A-Za-z]+(?:[ -][A-Za-z]+)*$", value):
        raise ValidationError("Name must contain only alphabetic characters, spaces and hyphens between words.")