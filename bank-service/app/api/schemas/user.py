from marshmallow import Schema, fields, validates, ValidationError, post_load

from app.models.role import Role
from app.extensions import db


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    roles = fields.List(fields.String(), required=True)
    is_blocked = fields.Bool()
    registered_on = fields.DateTime(dump_only=True)
    blocked_on = fields.DateTime(dump_only=True)
    last_login_date = fields.DateTime(dump_only=True)

    @post_load
    def convert_names_to_roles(self, input_data, **kwargs):
        """Converts role names from strings to objects so sqlalchemy model can show users.roles.
        This function is called when loading data from json to python object."""
        if "roles" in input_data:
            role_objects = Role.query.filter(
                Role.name.in_(input_data['roles'])).all()
            input_data['roles'] = role_objects
        return input_data


# the Meta class helps customize each schema for their purposes
class CreateUserSchema(UserSchema):
    class Meta:
        dump_only = ("is_blocked",)