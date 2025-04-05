from flask import request
from flask_jwt_extended import jwt_required, get_jwt

from app.commons.base_resources import BaseObjectResource, BaseListResource
from app.commons.constants import ACCESS_DENIED_ERROR
from app.models.client import Client
from app.api.schemas.client import ClientSchema
from app.auth.utils import user_roles_required


class ClientObjectRes(BaseObjectResource):
    model = Client
    schema = ClientSchema()

    method_decorators = [user_roles_required('admin', 'user'), jwt_required()]

    def get(self, id):
        jwt = get_jwt()
        if id != jwt.get('client_id'):
            return ACCESS_DENIED_ERROR

        return super().get(id)

    def put(self, id):
        jwt = get_jwt()
        if id != jwt.get('client_id'):
            return ACCESS_DENIED_ERROR

        return super().put(id)

    def delete(self, id):
        jwt = get_jwt()
        if id != jwt.get('client_id'):
            return ACCESS_DENIED_ERROR

        return super().delete(id)


class ClientListRes(BaseListResource):
    model = Client
    schema = ClientSchema()

    method_decorators = {
        'get': [user_roles_required('admin'), jwt_required()],
        'post': [user_roles_required('admin', 'user'), jwt_required()]
    }

    def post(self):
        if get_jwt().get('user_id') != request.json.get('user_id'):
            return ACCESS_DENIED_ERROR

        return super().post()
