import logging
from logging.handlers import RotatingFileHandler

from . import formatters


def console():
    ch = logging.StreamHandler()
    ch.setFormatter(formatters.Default())
    return ch


def file(filename, maxBytes=1024 * 1024 * 5, backupCount=5):
    return RotatingFileHandler(
        filename=filename,
        maxBytes=maxBytes,
        backupCount=backupCount,
    )
