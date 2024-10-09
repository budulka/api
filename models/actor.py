from datetime import datetime as dt

from core import db
from models.relations import association
from sqlalchemy import Date
from models.base import Model

class Actor(db.Model, Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(11))
    date_of_birth = db.Column(Date)
    movies = db.relationship(
            'Movie',
            secondary=association,
            backref=db.backref('cast', cascade="all, delete", uselist=True),            
            uselist=True,
            overlaps="filmography")

    def __repr__(self):
        return '<Actor {}>'.format(self.name)
