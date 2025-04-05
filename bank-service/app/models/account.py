from app.extensions import db
from app.models.card import Card


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False, default=0)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'clients.id', ondelete='CASCADE'))
    bank_id = db.Column(db.Integer, db.ForeignKey(
        'banks.id', ondelete='CASCADE'))

    cards = db.relationship('Card', backref='account', lazy=True)

    def __repr__(self):
        return f'Id: {self.id}, balance: {self.balance}, client_id: {self.client_id}, bank_id: {self.bank_id}'
