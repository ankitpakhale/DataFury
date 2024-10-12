# pylint: disable=pointless-string-statement
"""
Starting point of the project
"""

# standard library imports
import os
from typing import Callable, Any

# third-Party library imports
import bottle
from bottle import Bottle, request, response, static_file, run

# local application imports
from utils import cache
from utils import logger
from constant import status
from download_files import DownloadFiles
from dotenv import load_dotenv

load_dotenv()


def generate_response(
    status: bool, payload: dict, message: str, status_code: str
) -> dict:
    """
    generate_response returns the response in specific order
    """
    return {
        "status": status,
        "payload": payload,
        "message": message,
        "status_code": status_code,
    }


def safeguard(func: Callable[..., Any]) -> Callable[..., dict]:
    """
    safeguard is a decorator that adds caching functionality.
    It returns a structured response containing the result and error
    information in the following format:
    {
        'status': True | False,
        'payload': result | None,
        'message': 'Response generated successfully' | error message
        'status_code': 200 | 400 | 404 | 500 | etc.
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
                status_code=status.HTTP_200_OK,
            )
        # TODO: create EXCEPTION_MAP
        except (
            ValueError,
            TypeError,
            KeyError,
            Exception,
        ) as e:  # specific exceptions to catch
            logger.error("Error occured: %s", {str(e)})
            return generate_response(
                status=False,
                payload={},
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper


app = Bottle()


@app.route("/ping")
@safeguard
def health_check() -> dict:
    """
    health-check endpoint
    """
    return {"result": "PONG"}


@app.route("/download", method="POST")
@safeguard
def download_files() -> dict:
    """
    download_files endpoint
    """
    bucket_name: str = request.forms.bucket_name.strip()
    print("➡ 103 bucket_name:", bucket_name)
    if bucket_name == "test_default":
        bucket_name = os.getenv("BUCKET_NAME")
    __download = DownloadFiles(bucket_name=bucket_name)
    return __download


# @safeguard
@app.route(
    "/download-file", methods="GET"
)  # specifying GET method is not mendatory, just to follow same order it is methods
def download_file():
    file_path = request.query.file_path
    if not file_path or not os.path.exists(file_path):
        return {"error": "File not found"}, 404
    return static_file(file_path, root=".", download=True)


if __name__ == "__main__":
    bottle.debug(True)
    app.run(host="localhost", port=8080, reloader=True)
