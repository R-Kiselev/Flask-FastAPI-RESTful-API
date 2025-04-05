from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.extensions import db, pwd_context
from .user_role import UserRole
from .client import Client


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column("password", db.String(255), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False, unique=False)

    registered_on = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    blocked_on = db.Column(db.DateTime, nullable=True)
    last_login_date = db.Column(db.DateTime, nullable=True)

    roles = relationship('Role', secondary='user_roles',
                         back_populates='users', lazy=True)
    client = relationship('Client', backref='client', lazy=True)

    def __init__(self, email, password, roles, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.roles.extend(roles)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def block(self):
        self.is_blocked = True
        self.blocked_on = db.func.now()

    def unblock(self):
        self.is_blocked = False
        self.blocked_on = None

    def update_login_time(self):
        self.last_login_date = db.func.now()
