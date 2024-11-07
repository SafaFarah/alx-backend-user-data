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
    pattern = f'{separator}({"|".join(fields)})=[^;]*'
    return re.sub(pattern, f'{separator}\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """class to obfuscate specified fields in log records."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """Initialize the formatter with fields to be redacted."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with obfuscated fields.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
