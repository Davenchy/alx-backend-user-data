#!/usr/bin/env python3
""" log message obfuscated using regex """
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """ This function uses a regex to replace occurrences of certain fields.
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}', f'{f}={redaction}{separator}',
                         message, count=1)
    return message
