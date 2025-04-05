from app.extensions import db
from app.models.bank import Bank
from app.models.city import City


class Branch(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey(
        'banks.id', ondelete='CASCADE'))
    city_id = db.Column(db.Integer, db.ForeignKey(
        'cities.id', ondelete='CASCADE'))

    banks = db.relationship('Bank', backref='branch', lazy=True)
    cites = db.relationship('City', backref='branch', lazy=True)

    def __repr__(self):
        return f'Id: {self.id}, bank_id: {self.bank_id}, city_id: {self.city_id}'
