from flask_restful import request
from flask_jwt_extended import jwt_required, get_jwt

from app.commons.base_resources import BaseObjectResource, BaseListResource
from app.commons.constants import ACCESS_DENIED_ERROR
from app.models.card import Card
from app.api.schemas.card import CardSchema
from app.extensions import db
from app.commons.pagination import paginate
from app.auth.utils import user_roles_required


class CardObjectRes(BaseObjectResource):
    model = Card
    schema = CardSchema()

    method_decorators = [user_roles_required('admin', 'user'), jwt_required()]

    def get(self, id):
        jwt = get_jwt()

        card = db.session.query(Card).where(Card.id == id).first()
        if not card or card.account_id not in jwt.get('account_ids'):
            return ACCESS_DENIED_ERROR

        return super().get(id)

    def put(self, id):
        jwt = get_jwt()

        card = db.session.query(Card).where(Card.id == id).first()
        if not card or card.account_id not in jwt.get('account_ids'):
            return ACCESS_DENIED_ERROR

        return super().put(id)

    def delete(self, id):
        jwt = get_jwt()

        card = db.session.query(Card).where(Card.id == id).first()
        if not card or card.account_id not in jwt.get('account_ids'):
            return ACCESS_DENIED_ERROR

        return super().delete(id)


class AccountCardListRes(BaseListResource):
    model = Card
    schema = CardSchema()

    method_decorators = {
        'get': [user_roles_required('admin'), jwt_required()],
        'post': [user_roles_required('admin', 'user'), jwt_required()]
    }

    def get(self, account_id=None):
        query = Card.query.filter(Card.account_id == account_id)

        return paginate(query, self.schema)

    def post(self, account_id=None):
        jwt = get_jwt()

        if account_id not in jwt.get('account_ids'):
            return ACCESS_DENIED_ERROR

        req_body = request.json
        req_body['account_id'] = account_id

        return super().post()
