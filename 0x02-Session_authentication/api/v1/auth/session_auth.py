#!/usr/bin/env python3
""" Module of SessionAuth
"""
from .auth import Auth
from typing import List, TypeVar
from flask import request
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth Management Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a new session for user_id """
        if not user_id or type(user_id) is not str:
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user_id based on session_id """
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
