import logging
import logging.config

from . import formatters

logging.config.dictConfig({"disable_existing_loggers": True, "version": 1})


# TODO: deprecate
def __get_logger_TBD(name="DataFury", level="CRITICAL"):
    logger = logging.getLogger(name=name)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    ch = logging.StreamHandler()
    ch.setFormatter(formatters.Default())
    logger.addHandler(ch)
    logger.setLevel(level=level)
    return logger


# TODO: name must come from root directory
# TODO: dynamic level
def get_logger(name="DataFury", level="DEBUG"):
    logger = logging.getLogger(name=name)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    ch = logging.StreamHandler()
    ch.setFormatter(formatters.Default())
    logger.addHandler(ch)
    logger.setLevel(level=level)
    return logger
