#!/usr/bin/python3
""" Check response
"""
from models.user_session import UserSession
from sys import exit

if __name__ == "__main__":
    try:
        UserSession.load_from_file()
        nb_before = UserSession.count()

        from api.v1.auth.session_db_auth import SessionDBAuth
        sdba = SessionDBAuth()
        user_id = None
        session_id = sdba.create_session(user_id)
        if session_id is not None:
            print("create_session should return None if user_id is None: {}".format(session_id))
            exit(1)

        # validate in DB
        UserSession.load_from_file()
        nb_after = UserSession.count()
        if nb_after != nb_before:
            print("create_session with user_id = None should not generate a UserSession")
            exit(1)

        print("OK", end="")
    except Exception:
        import sys
        print("Error: {}".format(sys.exc_info()))
