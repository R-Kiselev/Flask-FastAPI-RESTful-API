from app.extensions import db
from app.models.account import Account


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    social_status_id = db.Column(db.Integer, db.ForeignKey(
        'social_statuses.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), unique=True)

    accounts = db.relationship('Account', backref='client', lazy=True)

    def __repr__(self):
        return f'Id: {self.id}, name: {self.name}, social_status_id: {self.social_status_id}'
