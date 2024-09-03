#!/usr/bin/env python3
""" Basic Authentication class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class inheriting from Auth.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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
