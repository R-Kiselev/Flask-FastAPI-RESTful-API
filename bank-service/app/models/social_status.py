from app.extensions import db
from app.models.client import Client


class SocialStatus(db.Model):
    __tablename__ = 'social_statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    clients = db.relationship('Client', backref='social_status', lazy=True)

    def __repr__(self):
        return f'Id: {self.id}, name: {self.name}'
