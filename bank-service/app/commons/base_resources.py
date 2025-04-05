from flask import request, jsonify
from flask_restful import Resource
from marshmallow import Schema
from app.extensions import db
from app.commons.pagination import paginate

class BaseObjectResource(Resource):
    model = None
    schema = Schema

    def get(self, id=None):
        item = self.model.query.get_or_404(id, description=f'The {self.model.__name__.lower()} with id = {id} was not found')
        return self.schema.dump(item), 200
            
    def put(self, id=None):
        item = self.model.query.get_or_404(id, description=f'The {self.model.__name__.lower()} with id = {id} does not exist')
        
        data = self.schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(item, key, value)

        db.session.commit()
        return {
            "msg": "item updated",
            "item": self.schema.dump(item)
        }, 200
           
    def delete(self, id=None):
        item = self.model.query.get_or_404(id, description=f'The {self.model.__name__.lower()} with id = {id} does not exist')

        db.session.delete(item)
        db.session.commit()

        return {
            "msg" : "item deleted",
            "item" : self.schema.dump(item)
        }, 200
    
class BaseListResource(Resource):
    model = None
    schema = Schema

    def get(self):
        query = self.model.query        
        return paginate(query, self.schema)
    
    def post(self):
        data = self.schema.load(request.json)
        item = self.model(**data)

        db.session.add(item)
        db.session.commit()

        return {
            "msg" : "item created",
            "item" : self.schema.dump(item)
        }, 201