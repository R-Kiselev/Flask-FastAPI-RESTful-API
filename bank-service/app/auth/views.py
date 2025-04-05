from flask import (
    Blueprint,
    jsonify,
    request
)
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_current_user,
    get_jwt
)

from app.extensions import pwd_context
from app.models.user import User
from app.auth.utils import user_roles_required
from app.api.schemas.user import UserSchema
from app.extensions import db

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=['POST'])
def register():
    '''Create a new user with default role 'user'.'''
    from app.api.resources.users import UserListResource

    request_data = request.json
    request_data['roles'] = ['user']

    return UserListResource().post()


@blueprint.route('/login', methods=['POST'])
def login():
    request_data = request.json
    credentials = UserSchema(only = ['email', 'password']).load(request_data)

    user = User.query.filter_by(email=credentials.get('email')).first()
    if not user or not pwd_context.verify(credentials.get('password'), user.password):
        return jsonify({'msg': 'Bad credentials'}), 400

    if (user.is_blocked):
        return jsonify({'err': 'Access denied. You are blocked'}), 401

    access_token = create_access_token(identity=user.id)

    user.update_login_time()
    db.session.commit()

    return jsonify({'access_token': access_token}), 200


@blueprint.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    '''Get current user and jwt payload info.'''
    current_user = get_current_user()
    token = get_jwt()

    claims = {
        'client_id': token.get('client_id'),
        'account_ids': token.get('account_ids'),
    }

    return jsonify({
        'user': UserSchema().dump(current_user),
        'token_claims': claims
    }), 200


@blueprint.route('/admin_required', methods=['GET'])
@jwt_required()
@user_roles_required('admin')
def admin_required():
    '''Only admin can access this route.'''
    return whoami()
