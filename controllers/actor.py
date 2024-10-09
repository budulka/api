from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor  
from models.movie import Movie
from settings.constants import ACTOR_FIELDS
from .parse_request import get_request_data

DATE_FORMAT = "%d.%m.%Y"

def get_all_actors():
    """
    Get list of all records
    """  
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200) 




def get_actor_by_id():
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error='No id specified'), 400)
    
    try:
        row_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error='Id must be integer'), 400)

    obj = Actor.query.filter_by(id=row_id).first()
    if obj is None:
        return make_response(jsonify(error='Record with such id does not exist'), 400)
    
    actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(actor), 200)


def add_actor():
    data = get_request_data()
    unexpected = [k for k in data.keys() if k not in ACTOR_FIELDS]
    if unexpected:
        return make_response(jsonify(error='Unexpected fields: ' + ', '.join(unexpected)), 400)
    
    required = ["name", "date_of_birth", "gender"]
    missing = [j for j in required if j not in data]
    if missing:
        return make_response(jsonify(error='Missing required fields: ' + ', '.join(missing)), 400)
    
    try:
        dt.strptime(data['date_of_birth'], DATE_FORMAT)
    except ValueError:
        return make_response(jsonify(error='Incorrect date format, should be DD.MM.YYYY'), 400)
    
    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)

def update_actor():
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error='No id specified'), 400)
    
    try:
        row_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error='Id must be integer'), 400)
    if 'date_of_birth' in data.keys():
        try:
            dt.strptime(data['date_of_birth'], DATE_FORMAT)
        except ValueError:
            return make_response(jsonify(error='Incorrect date format, should be DD.MM.YYYY'), 400)

    actor_to_upd = Actor.query.filter_by(id=row_id).first()
    if actor_to_upd is None:
        return make_response(jsonify(error="Actor not found"), 400)
    
    unexpected = [k for k in data.keys() if k not in ACTOR_FIELDS and k != 'id']
    if unexpected:
        return make_response(jsonify(error='Unexpected fields: ' + ', '.join(unexpected)), 400)
    
    upd_record = Actor.update(row_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)

def delete_actor():
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error="No id specified"), 400)

    
    try:
        row_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error='Id must be integer'), 400)
    act = Actor.query.filter_by(id=row_id).first()
    if act is None:
        return make_response(jsonify("Oh no!"), 400)
    try:
        Actor.clear_relations(row_id)
        Actor.delete(row_id)
    except:
        return make_response(jsonify(err="aaaee"), 400)
    return make_response(jsonify(message='Record successfully deleted'), 200)
    


def actor_add_relation():
    data = get_request_data()
    if 'id' not in data or 'relation_id' not in data:
        return make_response(jsonify(error='Both actor id and movie id are required'), 400)
    
    try:
        actor_id = int(data['id'])
        movie_id = int(data['relation_id'])
    except ValueError:
        return make_response(jsonify(error='Both ids must be integers'), 400)
    try:
        movie = Movie.query.get(movie_id)
    except:
        return make_response(jsonify(err="no id exists"), 400)
    if movie is None:
        return make_response(jsonify(error='Movie not found'), 400)
    try:
        actor = Actor.add_relation(actor_id, movie)
    except:
        return make_response(jsonify(err='no id actor'), 400)
    if actor is None:
        return make_response(jsonify(error='Actor not found'), 400)

    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)

def actor_clear_relations():
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error='No id specified'), 400)
    
    try:
        row_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error='Id must be integer'), 400)
    try:
        actor = Actor.clear_relations(row_id)
    except:
        return make_response(jsonify(err='pizdec'), 400)
    if actor is None:
        return make_response(jsonify(error='Actor not found'), 400)

    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
