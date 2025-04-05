from functools import wraps

from flask import jsonify, make_response
from flask_jwt_extended import (
    get_current_user
)

from app.extensions import db, jwt
from app.models.user import User
from app.models.client import Client
from app.models.account import Account


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_payload):
    '''Get user object from database.
    This function is called when a get_current_user() function is called.
    '''
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.additional_claims_loader
def load_client_and_accounts_id(user_identity):
    '''Callback function to add custom claims to the JWT token.
    This function is called when a create_access_token() function is called.
    '''
    claims = {}
    claims['user_id'] = user_identity

    client_id = db.session.query(Client.id)\
        .where(Client.user_id == user_identity)\
        .scalar()

    if not client_id:
        claims['client_id'] = None
        claims['account_ids'] = []
        return claims

    accounts = db.session.query(Account)\
        .where(Account.client_id == client_id)\
        .all()
    account_ids = [account.id for account in accounts]

    claims['client_id'] = client_id
    claims['account_ids'] = account_ids

    return claims


def user_roles_required(*required_roles):
    '''Decorator to check if user has required roles.
    This function checks if the current user has any of the required roles passed as arguments.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_current_user()

            if not any(role.name in required_roles for role in current_user.roles):
                return make_response(jsonify({'error': 'Access denied'}), 403)

            return func(*args, **kwargs)
        return wrapper
    return decorator
