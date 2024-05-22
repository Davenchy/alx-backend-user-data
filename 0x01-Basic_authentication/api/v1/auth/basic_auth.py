#!/usr/bin/env python3
""" Module of BasicAuth
"""
from .auth import Auth


class BasicAuth(Auth):
    """ Basic Auth Management class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ extracts the base64 token from authorization http header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]
