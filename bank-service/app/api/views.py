from flask import Blueprint
from flask_restful import Api

from app.api.resources.accounts import AccountObjectRes, AccountListRes, ClientAccountListRes
from app.api.resources.roles import RoleObjectRes, RoleListRes
from app.api.resources.users import UserObjectResource, UserListResource
from app.api.resources.cards import CardObjectRes, AccountCardListRes
from app.api.resources.branches import BranchObjectRes, BranchListRes
from app.api.resources.clients import ClientObjectRes, ClientListRes
from app.api.resources.social_statuses import SocialStatusObjectRes, SocialStatusListRes
from app.api.resources.cities import CityObjectRes, CityListRes
from app.api.resources.banks import BankObjectRes, BankListRes

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

# Banks
api.add_resource(BankListRes, '/banks')
api.add_resource(BankObjectRes, '/banks/<int:id>')

# Cities
api.add_resource(CityListRes, '/cities')
api.add_resource(CityObjectRes, '/cities/<int:id>')

# Social statuses
api.add_resource(SocialStatusListRes, '/social-statuses')
api.add_resource(SocialStatusObjectRes, '/social-statuses/<int:id>')

# Clients
api.add_resource(ClientListRes, '/clients')
api.add_resource(ClientObjectRes, '/clients/<int:id>')

# Branches
api.add_resource(BranchListRes, '/banks/<int:bank_id>/branches')
api.add_resource(BranchObjectRes, '/branches/<int:id>')

# Accounts
api.add_resource(AccountListRes, '/banks/<int:bank_id>/accounts')
api.add_resource(ClientAccountListRes, '/clients/<int:client_id>/accounts')
api.add_resource(AccountObjectRes, '/accounts/<int:id>')

# Cards
api.add_resource(AccountCardListRes, '/accounts/<int:account_id>/cards')
api.add_resource(CardObjectRes, '/cards/<int:id>')


# Users
api.add_resource(UserListResource, '/users')
api.add_resource(UserObjectResource, '/users/<int:id>')


# Roles
api.add_resource(RoleListRes, '/roles')
api.add_resource(RoleObjectRes, '/roles/<int:id>')
