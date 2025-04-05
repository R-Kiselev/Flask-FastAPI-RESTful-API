from sqlalchemy.orm import relationship

from app.extensions import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    users = relationship('User', secondary='user_roles',
                         back_populates='roles', lazy=True)

    def __repr__(self):
        return f'{self.name}'
