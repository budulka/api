from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor  
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        return make_response(jsonify(err="no id"), 400)
    try:
        row_id = int(data['id'])
    except ValueError:
        err = "Id must be integer"
        return make_response(jsonify(error=err), 400)
    obj = Movie.query.filter_by(id=row_id).first()
    if obj is None:
        return make_response(jsonify(err="no"), 400)
    
    movie_data = {k: getattr(obj, k) for k in MOVIE_FIELDS if hasattr(obj, k)}
    return make_response(jsonify(movie_data), 200)

def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    print(data.keys())
    unexpected = [k for k in data.keys() if k not in MOVIE_FIELDS]
    print(unexpected)
    if unexpected:
        msg = 'Unexpected fields'
        return make_response(jsonify(message = msg), 400)
    required_fields = ['name', 'genre', 'year']
    missing = [f for f in required_fields if f not in data.keys()]
    if missing:
        return make_response(jsonify(error="Insufficint data"), 400)
    try:
        data['year'] = int(data['year'])
    except ValueError:
        msg = 'Year must be int'
        return make_response(jsonify(message = msg), 400)
    new_record = Movie.create(**data)
    new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        return make_response(jsonify("no id"), 400)
    unexpected = [k for k in data.keys() if k not in MOVIE_FIELDS]
    if unexpected:
        msg = 'Unexpected fields'
        return make_response(jsonify(message = msg), 400) 
    try:
        row_id = int(data['id'])
    except ValueError:
        msg = "Id int"
        return make_response(jsonify(message = msg), 400)
    if 'year' in data.keys():
        try:
            data['year'] = int(data['year'])
        except ValueError:
            return make_response(jsonify(message="Year. wrong"), 400)
    movie_to_upd = Movie.query.filter_by(id=row_id).first()
    if movie_to_upd is None:
        return make_response(jsonify(error="Movie not found"), 400)
    upd_record = Movie.update(row_id, **data)
    upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(upd_movie), 200)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row = int(data['id'])
        except ValueError:
            msg = "Id must be int"
            return make_response(jsonify(message = msg), 400)
        movie_to_delete = Movie.query.filter_by(id=row).first()
        print(movie_to_delete)
        if movie_to_delete is None:
            return make_response(jsonify(error="Movie not found"), 400)
        #Movie.clear_relations(row)
        Movie.delete(row)
            #make_response(jsonify(error = "Idk what happened"),400)
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)
    else:
        return make_response(jsonify(error = 'no id specified'), 400)
    
def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    
    if 'id' not in data.keys() or 'relation_id' not in data.keys():
        return make_response(jsonify(err='id and actor_id required'), 400)
    
    try:
        movie_id = int(data['id'])
        actor_id = int(data['relation_id'])
    except ValueError:
        return make_response(jsonify(err='id and actor_id must be integers'), 400)
    try:
        actor = Actor.query.get(actor_id)
    except:
        return make_response(jsonify(err='no id exists'), 400)
    if actor is None:
        return make_response(jsonify(err="Actor not found"), 400)
    try:
        movie = Movie.add_relation(movie_id, actor)
    except:
        return make_response(jsonify(err='no id mov exists'), 400)
    if movie is None:
        return make_response(jsonify(err="Actor not found"), 400)
    
    rel_movie = {k: getattr(movie, k) for k in MOVIE_FIELDS if hasattr(movie, k)}
    rel_movie['cast'] = [actor.name for actor in movie.cast]
    return make_response(jsonify(rel_movie), 200)



def movie_clear_relations():
    """
    Clear all relations by movie id (i.e., remove all actors from the movie's cast)
    """
    data = get_request_data()
    if 'id' not in data.keys():
        return make_response(jsonify(error='Movie id not specified'), 400)

    try:
        row_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error='Movie id must be an integer'), 400)
     

    try:
        movie = Movie.clear_relations(row_id)
    except:
        return make_response(jsonify(error="no rels"), 400)
    if movie is None:
        return make_response(jsonify(error='Movie not found'), 400)

    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = []
    return make_response(jsonify(rel_movie), 200)
