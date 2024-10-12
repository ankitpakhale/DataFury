import logging
import diskcache as dc


# configure logging
logging.basicConfig(
    level=logging.ERROR,  # set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # log message format
)

# create a logger instance
logger = logging.getLogger(__name__)


# diskcache configurations
cache = dc.Cache("mycache")
