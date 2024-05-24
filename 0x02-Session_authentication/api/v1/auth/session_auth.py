#!/usr/bin/env python3
""" Module of SessionAuth
"""
from typing import TypeVar
from uuid import uuid4

from models.user import User
from .auth import Auth


class SessionAuth(Auth):
    """ Session Auth Management Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a new session for user_id """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user_id based on session_id """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ get the current user as provided in the session_id """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
