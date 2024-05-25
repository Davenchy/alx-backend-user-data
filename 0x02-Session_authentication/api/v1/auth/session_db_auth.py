#!/usr/bin/env python3
""" Module of SessionDBAuth
"""
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ Expirable Sessions Auth Manager class that stores sessions in DB
    """

    def create_session(self, user_id=None):
        """ Create session for user_id and set expiration time
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user_id registered for a session using session_id
        """
        UserSession.load_from_file()

        if not session_id or not isinstance(session_id, str):
            return None
        user_id = super().user_id_for_session_id(session_id)
        if user_id:
            return user_id

        session = UserSession.search({'session_id': session_id})
        return session[0].user_id if session else None

    def destroy_session(self, request=None) -> bool:
        """ delete/logout user by deleting session by its id if exist """
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        del self.user_id_by_session_id[session_id]
        sessions[0].remove()
        return True
