# pylint: disable=pointless-string-statement
"""
Starting point of the project
"""

from typing import Callable, Any
from utils import cache
from utils import logger
import bottle
from bottle import route, run, request


def generate_response(status: bool, payload: dict, message: str) -> dict:
    """
    generate_response returns the response in specific order
    """
    return {"status": status, "payload": payload, "message": message}


def safeguard(func: Callable[..., Any]) -> Callable[..., dict]:
    """
    safeguard is a decorator that adds caching functionality.
    It returns a structured response containing the result and error
    information in the following format:
    {
        'status': True | False,
        'payload': result | None,
        'message': 'Response generated successfully' | error message
    }
    """

    def wrapper(*args, **kwargs) -> dict:
        try:
            """
            It first checks if the requested key's data is present in the cache.
            If the data is found, it returns that data. If not, it makes the request,
            retrieves the response, and stores it in the cache for future use.
            """
            key: str = request.forms.url.strip()
            cached_data: dict = cache.get(key)
            if cached_data is None:
                result = func(*args, **kwargs)
                cache[key] = result
                logger.debug("Cached response of %s key", {key})
            else:
                result = cached_data
                logger.debug("Cached data found for %s key", {key})

            return generate_response(
                status=True,
                payload=result,
                message="Response generated successfully",
            )
        except (ValueError, TypeError, KeyError) as e:  # specific exceptions to catch
            logger.error("Error occured: %s", {str(e)})
            return generate_response(status=False, payload={}, message=str(e))
        except Exception as e:  # pylint: disable=broad-exception-caught
            # log unexpected exceptions
            logger.error(
                "Unexpected error in %s: %s", func.__name__, e
            )  # lazy % formatting
            return generate_response(
                status=False, payload={}, message="An unexpected error occurred."
            )

    return wrapper


@route("/ping")
@safeguard
def health_check():
    """
    health-check endpoint
    """
    return {"result": "PONG"}


@route("/download-files", method="POST")
@safeguard
def download_files():
    """
    download_files endpoint
    """
    url = request.forms.url.strip()
    print("➡ url:", url)
    return url


if __name__ == "__main__":
    bottle.debug(True)
    run(host="localhost", port=8080, reloader=True)
