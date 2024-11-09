#!/usr/bin/env python3
"""
Module to obfuscate specified fields in a log message.
"""

import re
from typing import List, Tuple
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): A list of field names to obfuscate.
        redaction (str): The string used to replace field values.
        message (str): The log message to be obfuscated.
        separator (str): The character separating fields in the message.

    Returns:
        str: The obfuscated log message.
    """
    # Create the regex pattern for fields
    pattern = r'(' + '|'.join(fields) + r')=[^' + re.escape(separator) + r']+'
    # Replace the values of the fields with the redaction
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)


def get_logger() -> logging.Logger:
    """Creates and returns logger configured to use the RedactingFormatter """
    # Create a logger named "user_data"
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler and set its formatter to RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ The constructor that contains a list of fields."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ method  filter values in incoming log records using filter_datum"""
        message = record.getMessage()
        record.msg = filter_datum(
                self.fields, self.REDACTION, message, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
