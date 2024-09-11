#!/usr/bin/env python3
"""
This module provides authentication-related functionalities for
the user authentication service.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _generate_uuid() -> str:
    """Generates a uuid.
    Returns:
        str: string representation of a new UUID.
    """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt.
    Args:
        password (str): The plaintext password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return the User object.
        If a user with the given email already exists, raise a ValueError.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user with the given email.
        - Returns the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve user by session ID."""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the given user ID."""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for the user."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token and new password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_password = _hash_password(password)
        self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None)
        return None
