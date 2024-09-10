#!/usr/bin/env python3
"""
This module provides authentication-related functionalities for
the user authentication service.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt.
    Args:
        password (str): The plaintext password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
