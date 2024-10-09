from core import db
from sqlalchemy import Table, Column, Integer, ForeignKey
association = db.Table('association', db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True), db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True))

# Table name -> 'association'
# Columns: 'actor_id' -> db.Integer, db.ForeignKey -> 'actors.id', primary_key = True
#          'movie_id' -> db.Integer, db.ForeignKey -> 'movies.id', primary_key = True

