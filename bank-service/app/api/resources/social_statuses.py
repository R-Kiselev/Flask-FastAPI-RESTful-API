from flask_jwt_extended import jwt_required

from app.commons.base_resources import BaseObjectResource, BaseListResource
from app.models.social_status import SocialStatus
from app.api.schemas.social_status import SocialStatusSchema
from app.auth.utils import user_roles_required


class SocialStatusObjectRes(BaseObjectResource):
    model = SocialStatus
    schema = SocialStatusSchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'put': [user_roles_required('admin', 'manager'), jwt_required()],
        'delete': [user_roles_required('admin', 'manager'), jwt_required()],
    }


class SocialStatusListRes(BaseListResource):
    model = SocialStatus
    schema = SocialStatusSchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'post': [user_roles_required('admin', 'manager'), jwt_required()]
    }
