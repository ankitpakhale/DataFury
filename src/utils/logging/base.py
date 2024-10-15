import os
import logging
import logging.config
from dotenv import load_dotenv

# load environment variables
load_dotenv()

from . import formatters

logging.config.dictConfig({"disable_existing_loggers": True, "version": 1})


# TODO: name must come from root directory
# TODO: dynamic level
def get_logger(name="DataFury", level="DEBUG"):
    __level = level if os.getenv("ENV") != "prod" else "CRITICAL"
    logger = logging.getLogger(name=name)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    ch = logging.StreamHandler()
    ch.setFormatter(formatters.Default())
    logger.addHandler(ch)
    logger.setLevel(level=__level)
    return logger
