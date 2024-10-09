import pytest
import requests

MOVIE_LIST_ROUTE = 'http://127.0.0.1:8000/api/movies'
MOVIE_ID_ROUTE = 'http://127.0.0.1:8000/api/movie'


@pytest.mark.parametrize(('body', 'expected_response'), [(dict([]), 200)])
def test_get_all_movies(body, expected_response):
    response = requests.get(MOVIE_LIST_ROUTE, data=body)
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body', 'expected_response'),
    [
        (dict(name='The Kings Man', genre='adventure', year='2021'), 200),
        (dict(name='Home Alone', genre='comedy', year='1990'), 200),
        (dict(name='Inception', year='2010'), 400), # all required fields should be specified
        (dict(name='Tenet', genre='sci-fi', year='2020', budget=100000), 400), # inputted fields should exist
        (dict(name='Interstellar', genre='sci-fi', year='2zero14'), 400) # year should be integer
    ]
)
def test_add_movie(body, expected_response):
    response = requests.post(MOVIE_ID_ROUTE, data=body)
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body', 'expected_response'),
    [
        (dict(name='Memento', genre='thriller', year='2000'), 200),
        (dict([]), 400), # id should be specified
        (dict(id='one'), 400), # id should be integer
        (dict(id=7**10), 400) # such movie id record should exist
    ]
)
def test_get_movie_by_id(body, expected_response):
    if expected_response == 200:
        post_response = requests.post(MOVIE_ID_ROUTE, data=body)
        body = dict(id=post_response.json()['id']) # get the movie id that was just created

    response = requests.get(MOVIE_ID_ROUTE, data=body)
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body_create', 'body_update', 'expected_response'),
    [
        (dict(name='The White Knight', genre='action', year='2008'),
             dict(name='The Dark Knight'), 200),
        (dict(name='Shutter Island', genre='comedy', year='2010'),
            dict(genre='thriller'), 200),
        (dict(name='Django Unchained', genre='western', year='2010'),
            dict(year='2012'), 200),
        (dict(name='The Matrix', genre='comedy', year='2009'),
            dict(genre='sci-fi', year='1999'), 200),
        (dict(name='Man of Steel', genre='adventure', year='2013'),
            dict(id=None), 400), # no id specified
        (dict(name='Spectre', genre='action', year='2015'),
            dict(id='one'), 400), # id must be integer
        (dict(name='Fight Club', genre='drama', year='1999'),
            dict(id=7**10), 400), # such movie id record should exist
        (dict(name='Transcendence', genre='sci-fi', year='2014'),
            dict(budget=100000), 400), # inputted field should exist
        (dict(name='Dune', genre='adventure', year='2021'),
            dict(year='twozerotwoone'), 400) # year should be integer
    ]
)
def test_update_movie(body_create, body_update, expected_response):
    post_response = requests.post(MOVIE_ID_ROUTE, data=body_create)
    movie_id = dict(id=post_response.json()['id'])  # get the movie id that was just created

    response = requests.put(MOVIE_ID_ROUTE, data={**movie_id, **body_update})
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body', 'expected_response'),
    [
        (dict(name='Argo', genre='drama', year='2012'), 200),
         (dict([]), 400), # id should be specified
        (dict(id='one'), 400), # id should be integer
        (dict(id=7**10), 400) # such movie id record should exist
    ]
)
def test_delete_movie(body, expected_response):
    if expected_response == 200:
        post_response = requests.post(MOVIE_ID_ROUTE, data=body)
        body = dict(id=post_response.json()['id'])  # get the movie id that was just created

    response = requests.delete(MOVIE_ID_ROUTE, data=body)
    assert response.status_code == expected_response
