#!/usr/bin/env python3
""" E2E integration tests for the API """
import requests

BASE_URL = "http://127.0.0.1:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test user registeration """
    res = requests.post(f'{BASE_URL}/users',
                        data={'email': email, 'password': password})
    assert res.status_code == 200

    data = res.json()
    assert data['email'] == email
    assert data['message'] == 'user created'

    res = requests.post(f'{BASE_URL}/users',
                        data={'email': email, 'password': password})
    assert res.status_code == 400

    data = res.json()
    assert data['message'] == 'email already registered'


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test log in with wrong password """
    res = requests.post(f'{BASE_URL}/sessions',
                        data={'email': email, 'password': password})
    assert res.status_code == 401


def profile_unlogged() -> None:
    """ Test profile with unlogged user """
    res = requests.get(f'{BASE_URL}/profile')
    assert res.status_code == 403


def log_in(email: str, password: str) -> str:
    """ Test log in """
    res = requests.post(f'{BASE_URL}/sessions',
                        data={'email': email, 'password': password})
    assert res.status_code == 200
    data = res.json()
    assert data['email'] == email
    assert data['message'] == 'logged in'

    session_id = res.cookies.get('session_id')
    assert session_id is not None

    return session_id


def profile_logged(session_id: str) -> None:
    """ Test profile with logged user """
    res = requests.get(f'{BASE_URL}/profile',
                       cookies={'session_id': session_id})
    assert res.status_code == 200
    data = res.json()
    assert data['email'] == EMAIL


def log_out(session_id: str) -> None:
    """ Test log out """
    res = requests.delete(f'{BASE_URL}/sessions',
                          cookies={'session_id': session_id})
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """ Test reset password token """
    res = requests.post(f'{BASE_URL}/reset_password', data={'email': email})
    assert res.status_code == 200
    data = res.json()
    assert data['email'] == email
    assert data['reset_token'] is not None
    return data['reset_token']


def update_password(email: str, reset_token: str, password: str) -> None:
    """ Test update password using reset token """
    res = requests.put(f'{BASE_URL}/reset_password',
                       data={'email': email, 'reset_token': reset_token,
                             'new_password': password})
    assert res.status_code == 200


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
