# pylint: disable=import-error
import bottle
import logging
from bottle import route, run, request
from typing import Callable, Any

# FIXME: Add caching in all the endpoints

# configure logging
logging.basicConfig(level=logging.ERROR)


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
            result: dict = {
                "status": True,
                "payload": func(*args, **kwargs),
                "message": "Response generated successfully",
            }
            print("➡ 22 result:", result)
            return result
        except (ValueError, TypeError, KeyError) as e:  # specific exceptions to catch
            return {"status": False, "payload": None, "message": str(e)}
        except Exception as e:  # pylint: disable=broad-exception-caught
            # log unexpected exceptions
            logging.error(f"Unexpected error in {func.__name__}: {e}")
            # logging.error(
            #     "Unexpected error in %s: %s", func.__name__, e
            # )  # lazy % formatting
            return {
                "status": False,
                "payload": None,
                "message": "An unexpected error occurred.",
            }

    return wrapper


@route("/ping")
@safeguard
def health_check():
    """
    health-check endpoint
    """
    return "PONG"


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
