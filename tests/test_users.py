from app.schema import *
from database import client, session
#from jose import jwt
import pytest



def test_root(client):
    response = client.get('/')
    assert response.json().get('message') == 'Hello World'

def test_create_user(client):
    response = client.post('/users/', json={"email":"hello3@gmail.com",
                                           "password": "Tuktuk123"})
    new_user = UserCreateResponse(**response.json())
    assert new_user.email == 'hello3@gmail.com'
    assert response.status_code == 201

def test_login_user(client):
    response = client.post('/login', data={"username":"hello3@gmail.com",
                                           "password": "Tuktuk123"})
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
