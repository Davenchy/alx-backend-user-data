#!/usr/bin/env python3
""" Module of BasicAuth
"""
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User
from base64 import decodebytes


class BasicAuth(Auth):
    """ Basic Auth Management class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ extracts the base64 token from authorization http header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ decode base64 authorization http header token """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = decodebytes(base64_authorization_header.encode('utf-8'))
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ extracts user credentials(email, password) from base64 token"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if decoded_base64_authorization_header.find(':') == -1:
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ get User object from authorization credentials """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
            if not user:
                return None
            user = user[0]
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ get the current user as provided in the request auth token """
        token = self.authorization_header(request)
        token = self.extract_base64_authorization_header(token)
        token = self.decode_base64_authorization_header(token)
        email, pwd = self.extract_user_credentials(token)
        return self.user_object_from_credentials(email, pwd)
