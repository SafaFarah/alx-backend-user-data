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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        _path = path.rstrip('/')
        for excluded_path in excluded_paths:
            _excluded_path = excluded_path.rstrip('/')
            if _path == _excluded_path:
                return False
            if _excluded_path.endswith('*'):
                prefix = _excluded_path[:-1]
                if _path.startswith(prefix):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None. Request will be the Flask request object.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None. Request will be the Flask request object.
        """
        return None
