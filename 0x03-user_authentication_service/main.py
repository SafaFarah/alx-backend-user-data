#!/usr/bin/env python3
""" This module sends HTTP requests to test registration, login,
    profile access, logout, password reset, and update functionalities
    using the `requests` module.
"""

import requests
from app import AUTH

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(f"{BASE_URL}/users",
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Try logging in with the wrong password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in a user and return the session_id."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Access the profile page without being logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access the profile page while logged in."""
    cookies = {'session_id': session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Log out a logged-in user."""
    cookies = {'session_id': session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={'email': email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password with a reset token."""
    response = requests.put(f"{BASE_URL}/reset_password", data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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
