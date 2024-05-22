#!/usr/bin/env python3
""" Module of BasicAuth
"""
from typing import Tuple
from .auth import Auth
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
