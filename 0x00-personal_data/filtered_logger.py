#!/usr/bin/env python3
""" log message obfuscated using regex """
from typing import List
import logging
import re

PII_FIELDS = ('name', 'email' 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """ create logger and return back """
    logger = logging.Logger("user_data", logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the log record """
        record.msg = filter_datum(self._fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)
