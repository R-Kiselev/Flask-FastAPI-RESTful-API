from flask_jwt_extended import jwt_required
from flask_restful import request

from app.commons.base_resources import BaseObjectResource, BaseListResource
from app.models.branch import Branch
from app.api.schemas.branch import BranchSchema
from app.commons.pagination import paginate
from app.auth.utils import user_roles_required


class BranchObjectRes(BaseObjectResource):
    model = Branch
    schema = BranchSchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'put': [user_roles_required('admin', 'manager'), jwt_required()],
        'delete': [user_roles_required('admin', 'manager'), jwt_required()]
    }


class BranchListRes(BaseListResource):
    schema = BranchSchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'post': [user_roles_required('admin', 'manager'), jwt_required()]
    }

    def get(self, bank_id=None):
        query = Branch.query.filter(Branch.bank_id == bank_id)
        return paginate(query, self.schema)

    def post(self, bank_id=None):
        req = request.json
        req['bank_id'] = bank_id

        return super().post()
