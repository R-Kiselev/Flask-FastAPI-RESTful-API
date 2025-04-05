from flask_jwt_extended import jwt_required

from app.commons.base_resources import BaseObjectResource, BaseListResource
from app.models.city import City
from app.api.schemas.city import CitySchema
from app.auth.utils import user_roles_required


class CityObjectRes(BaseObjectResource):
    model = City
    schema = CitySchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'put': [user_roles_required('admin', 'manager'), jwt_required()],
        'delete': [user_roles_required('admin', 'manager'), jwt_required()]
    }


class CityListRes(BaseListResource):
    model = City
    schema = CitySchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'post': [user_roles_required('admin', 'manager'), jwt_required()]
    }
