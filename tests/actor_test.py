import pytest
import requests

ACTOR_LIST_ROUTE = 'http://127.0.0.1:8000/api/actors'
ACTOR_ID_ROUTE = 'http://127.0.0.1:8000/api/actor'


@pytest.mark.parametrize(('body', 'expected_response'), [(dict([]), 200)])
def test_get_all_actors(body, expected_response):
    response = requests.get(ACTOR_LIST_ROUTE, data=body)
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body', 'expected_response'),
    [
        (dict(name='Megan Fox', gender='female', date_of_birth='01.01.1970'), 200),
        (dict(name='Shia LaBeouf', gender='male', date_of_birth='05.11.1986'), 200),
        (dict(name='Jesse Plemons', date_of_birth='04.02.1988'), 400), # all required fields should be specified
        (dict(name='Bryce Dallas Howard', gender='female', date_of_birth='03.02.1981', salary=170000), 400), # inputted fields should exist
        (dict(name='Tom Holland', gender='male', date_of_birth='06/02/1996'), 400) # date of birth should be in format DATE_FORMAT
    ]
)
def test_add_actor(body, expected_response):
    response = requests.post(ACTOR_ID_ROUTE, data=body)
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body', 'expected_response'),
    [
        (dict(name='Garrett Hedlund', gender='male', date_of_birth='09.03.1984'), 200),
        (dict([]), 400), # id should be specified
        (dict(id='one'), 400), # id should be integer
        (dict(id=7**10), 400) # such actor id record should exist
    ]
)
def test_get_actor_by_id(body, expected_response):
    if expected_response == 200:
        post_response = requests.post(ACTOR_ID_ROUTE, data=body)
        body = dict(id=post_response.json()['id']) # get the actor id that was just created

    response = requests.get(ACTOR_ID_ROUTE, data=body)
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    ('body_create', 'body_update', 'expected_response'),
    [
        (dict(name='Zonda', gender='female', date_of_birth='09.01.1996'),
            dict(name='Zendaya'), 200),
        (dict(name='Sigourney Weaver', gender='male', date_of_birth='10.08.1949'),
             dict(gender='female'), 200),
         (dict(name='Eddie Murphy', gender='male', date_of_birth='01.01.1970'),
             dict(date_of_birth='04.03.1961'), 200),
         (dict(name='Antonio Banderas', gender='female', date_of_birth='04.03.1961'),
             dict(gender='male',date_of_birth='08.10.1960'), 200),
         (dict(name='Peter Greene', gender='male', date_of_birth='10.08.1965'),
             dict(id=None), 400), # no id specified
        (dict(name='Adriano Celentano', gender='male', date_of_birth='01.06.1938'),
            dict(id='one'), 400), # id must be integer
        (dict(name='Ornella Muti', gender='female', date_of_birth='03.09.1955'),
            dict(id=7**10), 400), # such actor id record should exist
        (dict(name='Naike Rivelli', gender='female', date_of_birth='10.10.1974'),
            dict(salary=100000), 400), # inputted field should exist
        (dict(name='Manou Lubowski', gender='male', date_of_birth='11.06.1969'),
            dict(date_of_birth='11/06/1969'), 400) # date of birth should be in format DATE_FORMAT
    ]
)
def test_update_actor(body_create, body_update, expected_response):
    post_response = requests.post(ACTOR_ID_ROUTE, data=body_create)
    actor_id = dict(id=post_response.json()['id'])  # get the actor id that was just created

    response = requests.put(ACTOR_ID_ROUTE, data={**actor_id, **body_update})
    assert response.status_code == expected_response


@pytest.mark.parametrize(('body', 'expected_response'),
    [
        (dict(name='Dwayne Johnson', gender='male', date_of_birth='05.09.1972'), 200),
        (dict([]), 400), # id should be specified
        (dict(id='one'), 400), # id should be integer
        (dict(id=7**10), 400) # such actor id record should exist
    ]
)
def test_delete_actor(body, expected_response):
    if expected_response == 200:
        post_response = requests.post(ACTOR_ID_ROUTE, data=body)
        body = dict(id=post_response.json()['id'])  # get the actor id that was just created

    response = requests.delete(ACTOR_ID_ROUTE, data=body)
    assert response.status_code == expected_response