#!/usr/bin/env python3
""" Module of SessionAuth
"""
from .auth import Auth
from typing import List, TypeVar
from flask import request


class SessionAuth(Auth):
    """ Session Auth Management Class """
