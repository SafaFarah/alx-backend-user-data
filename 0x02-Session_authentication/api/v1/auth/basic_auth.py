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
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves User instance for a given request use Basic Authentication.
        Args:
            request: The Flask request object.
        Returns:
            User: The User instance if credentials are valid.
            None: If there error with credentials or the user is not found.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        dec_auth_header = self.decode_base64_authorization_header(base64_auth)
        if dec_auth_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(dec_auth_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
