#!/usr/bin/env python3
""" Module of Auth
"""
from os import getenv
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth Management Class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ set path as authentication required """
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'

        for p in excluded_paths:
            if p[-1] == '*':
                if path.startswith(p[:-1]):
                    return False
                continue

            if p[-1] != '/':
                p += '/'

            if p == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ get the current request authentication header """
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ get the current user detected by the authentication process """
        return None

    def session_cookie(self, request=None):
        """ get the session cookie value
        use the env var SESSION_NAME to set the cookie name
        the default value of SESSION_NAME is '_my_session_id'"""
        if request is None:
            return None

        cookie_name = getenv('SESSION_NAME') or '_my_session_id'
        return request.cookies.get(cookie_name)
