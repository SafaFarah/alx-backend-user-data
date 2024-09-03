#!/usr/bin/env python3
""" Module to manage API authentication """
from typing import List, TypeVar
from flask import request


class Auth:
    """ Class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False. Path and excluded_paths are not used currently.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None. Request will be the Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None. Request will be the Flask request object.
        """
        return None
