#!/usr/bin/env python3
""" Module of Auth
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth Management Class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ set path as authentication required """
        return False

    def authorization_header(self, request=None) -> str:
        """ get the current request authentication header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ get the current user detected by the authentication process """
        return None
