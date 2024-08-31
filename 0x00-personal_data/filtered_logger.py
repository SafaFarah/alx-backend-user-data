#!/usr/bin/env python3
"""
Module to obfuscate specified fields in a log message.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
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
