from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.commons.base_resources import BaseListResource, BaseObjectResource
from app.models.user import User
from app.api.schemas.user import UserSchema, CreateUserSchema
from app.auth.utils import user_roles_required
from app.models.role import Role
from app.models.user import User


class UserObjectResource(BaseObjectResource):
    model = User
    schema = UserSchema()

    method_decorators = [user_roles_required('admin'), jwt_required()]

    def put(self, id):
        user = User.query.get_or_404(id)
        user_data = self.schema.load(request.json)

        if user_data.get('is_blocked') and not user.is_blocked:
            user.block()
        elif not user_data.get('is_blocked') and user.is_blocked:
            user.unblock()

        return super().put(id)


def get_invalid_roles(user_roles):
    existing_roles = {role.name for role in Role.query.all()}
    invalid_roles = user_roles - existing_roles
    return invalid_roles


class UserListResource(BaseListResource):
    model = User

    method_decorators = [user_roles_required('admin'), jwt_required()]

    def get(self):
        self.schema = UserSchema(many=True)

        return super().get()

    def post(self):
        self.schema = CreateUserSchema()

        user_data = self.schema.dump(request.json)

        user = User.query.filter_by(email=user_data.get('email')).first()
        if user:
            return jsonify({
                'err': 'User already exists'
            }), 409

        invalid_roles = get_invalid_roles(set(user_data.get('roles', [])))
        if invalid_roles:
            return jsonify({
                'err': f"Roles {invalid_roles} do not exist"
            }), 400

        return super().post()
