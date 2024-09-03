#!/usr/bin/env python3
""" Basic Authentication class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic authentication class inheriting from Auth.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header.
            Args:
                authorization_header (str): The Authorization header.
            Returns:
                str: Base64 part of the Authorization header if valid,or None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes a Base64 authorization header to a UTF-8 string.
        Args:
            base64_authorization_header (str): The Base64 authorization header.
        Returns:
            str: The decoded UTF-8 string if valid, else None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts  (email and password) from the decoded Base64.
        Args:
            decoded_base64_authorization_header:decoded Base64 authorization.
        Returns:
            tuple: containing the email and password if valid,or (None, None).
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password.
        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.
        Returns:
            User: The User instance if the credentials are valid.
            None: If the email or password is invalid,
            or if no user is with the given email.
        """
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None
        user = User.search({"email": user_email})
        if not user:
            return None
        user = user[0]
        if user.is_valid_password(user_pwd):
            return user
        return None
