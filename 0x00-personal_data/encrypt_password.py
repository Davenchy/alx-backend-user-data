#!/usr/bin/env python3
""" Hash passwords before storing it """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Salt and hash password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check and validate password """
    return bcrypt.checkpw(password.encode(), hashed_password)
