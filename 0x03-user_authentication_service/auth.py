#!/usr/bin/env python3
"""
Auth module
"""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    Hash password with salt using bcrypt
    """
    return hashpw(password.encode('utf-8'), gensalt())
