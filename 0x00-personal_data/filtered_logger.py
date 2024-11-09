#!/usr/bin/env python3
"""
Module to obfuscate specified fields in a log message.
"""

import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """ The constructor that contains a list of fields."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ method  filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
