#!/usr/bin/env python3
""" Hash passwords before storing it """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Salt and hash password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
