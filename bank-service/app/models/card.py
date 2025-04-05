from app.extensions import db


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False, default=0)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'accounts.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'Id: {self.id}, balance: {self.balance}, account_id: {self.account_id}'
