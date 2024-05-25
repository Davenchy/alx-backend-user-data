#!/usr/bin/env python3
""" Module of SessionExpAuth
"""
from os import getenv
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Expirable Sessions Auth Manager class
    """

    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create session for user_id and set expiration time
        """

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user_id registered for a session using session_id
        """
        if not session_id:
            return None

        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None

        user_id = session['user_id']
        if self.session_duration <= 0:
            return user_id

        if 'created_at' not in session:
            return None

        created_at = session['created_at']
        expired_at = created_at + timedelta(seconds=self.session_duration)
        return None if expired_at < datetime.now() else user_id
