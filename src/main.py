"""
Starting point of the project
"""

import logging
from typing import Callable, Any
import bottle
from bottle import route, run, request

# FIXME: Add caching in all the endpoints

# configure logging
logging.basicConfig(level=logging.ERROR)


def generate_response(status: bool, payload: dict, message: str) -> dict:
    """
    generate_response returns the response in specific order
    """
    return {"status": status, "payload": payload, "message": message}


def safeguard(func: Callable[..., Any]) -> Callable[..., dict]:
    """
    safeguard is a decorator that provides result & error in specific order.
    It follows this order
    {
        'status': True | False,
        'payload': result | None,
        'message': Response generated successfully | error msg
    }
    """

    def wrapper(*args, **kwargs) -> dict:
        try:
            return generate_response(
                status=True,
                payload=func(*args, **kwargs),
                message="Response generated successfully",
            )
        except (ValueError, TypeError, KeyError) as e:  # specific exceptions to catch
            return generate_response(status=False, payload={}, message=str(e))
        except Exception as e:  # pylint: disable=broad-exception-caught
            # log unexpected exceptions
            logging.error(
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
    return url


if __name__ == "__main__":
    bottle.debug(True)
    run(host="localhost", port=8080, reloader=True)
