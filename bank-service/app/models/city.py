from app.extensions import db


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f'Id: {self.id}, name: {self.name}'
