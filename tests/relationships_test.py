import pytest
import requests

ACTOR_ID_ROUTE = 'http://127.0.0.1:8000/api/actor'
ACTOR_REL_ROUTE = 'http://127.0.0.1:8000/api/actor-relations'

MOVIE_ID_ROUTE = 'http://127.0.0.1:8000/api/movie'
MOVIE_REL_ROUTE = 'http://127.0.0.1:8000/api/movie-relations'


@pytest.mark.parametrize(
    ('body_add_actor','actor_id_corrected', 'body_add_movie','movie_id_corrected', 'expected_response'),
    [
        (dict(name='Jaeden Martell', gender='male', date_of_birth='01.04.2003'),{},
            dict(name='It', genre='horror', year='2017'),{}, 200),
        (dict(name='Zazie Beetz', gender='female', date_of_birth='06.01.1991'),{'id':None}, # no actor id specified
            dict(name='Joker', genre='thriller', year='2019'),{}, 400),
        (dict(name='Sam Worthington', gender='male', date_of_birth='08.02.1976'),{}, # no movie id specified
            dict(name='Hacksaw Ridge', genre='drama', year='2016'),{'relation_id':None}, 400),
        (dict(name='Morena Baccarin', gender='female', date_of_birth='06.03.1979'),{'id': 'one'}, # actor id should be integer
            dict(name='Deadpool', genre='action', year='2016'),{}, 400),
        (dict(name='Jeremy Renner', gender='male', date_of_birth='01.07.1971'),{}, # movie id should be integer
            dict(name='Arrival', genre='sci-fi', year='2016'),{'relation_id':'one'}, 400),
        (dict(name='Roman Griffin Davis', gender='male', date_of_birth='03.05.2007'),{'id': 7**10}, # actor id record should exist
            dict(name='Jojo Rabbit', genre='war', year='2019'),{}, 400),
        (dict(name='Caleb Landry Jones', gender='male', date_of_birth='12.07.1989'),{}, # movie id record should exist
            dict(name='The Outpost', genre='history', year='2019'),{'relation_id':7**10}, 400)
    ]
)
def test_actor_add_relation(body_add_actor, actor_id_corrected, movie_id_corrected, body_add_movie, expected_response):
    actor_id = requests.post(ACTOR_ID_ROUTE, data=body_add_actor).json()['id']
    movie_id = requests.post(MOVIE_ID_ROUTE, data=body_add_movie).json()['id']

    # add relation to actor
    body_add_rel = dict(id=actor_id, relation_id=movie_id)
    resp_add_rel = requests.put(ACTOR_REL_ROUTE, data={**body_add_rel, **actor_id_corrected, **movie_id_corrected})

    assert resp_add_rel.status_code == expected_response


@pytest.mark.parametrize(
    ('body_add_actor','actor_id_corrected', 'body_add_movie', 'expected_response'),
    [
        (dict(name='Keanu Reeves', gender='male', date_of_birth='09.02.1964'),{},
            dict(name='John Wick', genre='crime', year='2014'), 200),
        (dict(name='Alicia Vikander', gender='female', date_of_birth='10.03.1988'), {'id':None}, # id should be specified
            dict(name='Ex Machina', genre='sci-fi', year='2014'), 400),
        (dict(name='Sasha Luss', gender='female', date_of_birth='06.06.1992'), {'id':'one'}, # id should be integer
            dict(name='Anna', genre='thriller', year='2019'), 400),
        (dict(name='Tom Hanks', gender='male', date_of_birth='07.09.1956'), {'id':7**10}, # such actor id record should exist
            dict(name='The Green Mile', genre='drama', year='1999'), 400)
    ]
)
def test_delete_actor_relation(body_add_actor, actor_id_corrected, body_add_movie, expected_response):
    actor_id = requests.post(ACTOR_ID_ROUTE, data=body_add_actor).json()['id']
    movie_id = requests.post(MOVIE_ID_ROUTE, data=body_add_movie).json()['id']

    # add relation to actor
    body_add_rel = dict(id=actor_id, relation_id=movie_id)
    requests.put(ACTOR_REL_ROUTE, data=body_add_rel)

    # clear relation
    body_clear_rels = dict(id=actor_id)
    resp_clear_rels = requests.delete(ACTOR_REL_ROUTE, data={**body_clear_rels, **actor_id_corrected})

    assert resp_clear_rels.status_code == expected_response


@pytest.mark.parametrize(
    ('body_add_movie','movie_id_corrected', 'body_add_actor','actor_id_corrected', 'expected_response'),
    [
        (dict(name='The Nun', genre='mystery', year='2018'),{},
            dict(name='Demián Bichir', gender='male', date_of_birth='08.01.1963'),{}, 200),
        (dict(name='We Bought a Zoo', genre='comedy', year='2011'), {'id':None}, # no movie id specified
            dict(name='Matt Damon', gender='male', date_of_birth='10.08.1970'), {}, 400),
        (dict(name='Passengers', genre='sci-fi', year='2016'),{}, # no actor id specified
            dict(name='Michael Sheen', gender='male', date_of_birth='02.05.1969'),{'relation_id':None}, 400),
        (dict(name='Lucy', genre='thriller', year='2014'),{'id':'one'}, # movie id should be integer
            dict(name='Morgan Freeman', gender='male', date_of_birth='06.01.1937'),{}, 400),
        (dict(name='Godzilla', genre='sci-fi', year='2014'), {}, # actor id should be integer
            dict(name='Bryan Cranston', gender='male', date_of_birth='03.07.1956'), {'relation_id':'one'}, 400),
        (dict(name='300', genre='action', year='2006'),{'id':7**10}, # movie id record should exist
            dict(name='Lena Headey', gender='female', date_of_birth='10.03.1973'),{}, 400),
        (dict(name='A Quiet Place', genre='horror', year='2018'),{}, # actor id record should exist
            dict(name='Millicent Simmonds', gender='female', date_of_birth='03.06.2003'),{'relation_id':7**10}, 400)
    ]
)
def test_movie_add_relation(body_add_movie, movie_id_corrected, body_add_actor, actor_id_corrected,  expected_response):
    movie_id = requests.post(MOVIE_ID_ROUTE, data=body_add_movie).json()['id']
    actor_id = requests.post(ACTOR_ID_ROUTE, data=body_add_actor).json()['id']

    # add relation to movie
    body_add_rel = dict(id=movie_id, relation_id=actor_id)
    resp_add_rel = requests.put(MOVIE_REL_ROUTE, data={**body_add_rel, **movie_id_corrected,  **actor_id_corrected})

    assert resp_add_rel.status_code == expected_response


@pytest.mark.parametrize(
    ('body_add_movie','movie_id_corrected', 'body_add_actor', 'expected_response'),
    [
        (dict(name='Extraction', genre='thriller', year='2020'), {},
            dict(name='Chris Hemsworth', gender='male', date_of_birth='08.11.1983'), 200),
        (dict(name='In Time', genre='sci-fi', year='2011'), {'id':None}, # id should be specified
            dict(name='Amanda Seyfried', gender='female', date_of_birth='12.03.1985'), 400),
        (dict(name='Official Secrets', genre='crime', year='2019'), {'id':'one'}, # id should be integer
            dict(name='Matthew Goode', gender='male', date_of_birth='04.03.1978'), 400),
        (dict(name='The Town', genre='thriller', year='2010'), {'id':7**10}, # such movie id record should exist
            dict(name='Rebecca Hall', gender='female', date_of_birth='03.03.1982'), 400)
    ]
)
def test_delete_movie_relation(body_add_movie, movie_id_corrected, body_add_actor, expected_response):
    movie_id = requests.post(MOVIE_ID_ROUTE, data=body_add_movie).json()['id']
    actor_id = requests.post(ACTOR_ID_ROUTE, data=body_add_actor).json()['id']

    # add relation to movie
    body_add_rel = dict(id=movie_id, relation_id=actor_id)
    requests.put(MOVIE_REL_ROUTE, data=body_add_rel)

    # clear relation
    body_clear_rels = dict(id=movie_id)
    resp_clear_rels = requests.delete(MOVIE_REL_ROUTE, data={**body_clear_rels, **movie_id_corrected})

    assert resp_clear_rels.status_code == expected_response
