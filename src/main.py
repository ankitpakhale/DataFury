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
from utils import cache_manager
from utils import logger
from download_files import DownloadFiles
from dotenv import load_dotenv


# load environment variables
load_dotenv()

# caching flag
IS_CACHING_REQUIRED: bool = False


def generate_response(
    status: bool, payload: dict, message: str, status_code: int
) -> dict:
    """
    generate_response returns the response in specific order
    """
    response.status = status_code
    return {
        "status": status,
        "payload": payload,
        "message": message,
        "status_code": status_code,
    }


def set_cors_headers():
    """
    function to handle CORS
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"


def safeguard(is_file_download: bool = False):
    """
    safeguard decorator handles caching and response logic for both regular and file download responses.
    :param is_file_download: A flag to specify if it's for a file download.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            try:
                # set cors headers
                set_cors_headers()

                # determine the key for caching
                key: str = (
                    request.query.file_path.strip()
                    if is_file_download
                    else request.forms.bucket_name.strip()
                )

                # caching logic
                if not IS_CACHING_REQUIRED:
                    logger.critical("Caching is OFF, turn it ON")

                if IS_CACHING_REQUIRED and cache_manager.has(key):
                    cached_result = cache_manager.get(key)
                    return (
                        cached_result
                        if is_file_download
                        else generate_response(
                            status=True,
                            payload=cached_result,
                            message="Cached response",
                            status_code=200,
                        )
                    )

                # execute the wrapped function
                result = func(*args, **kwargs)

                # cache the result
                if IS_CACHING_REQUIRED:
                    cache_manager.set(key, result)

                # handle file downloads differently
                if is_file_download:
                    return result

                # generate a standard response
                return generate_response(
                    status=True,
                    payload=result,
                    message="Response generated successfully",
                    status_code=200,
                )

            except (ValueError, TypeError, KeyError) as e:
                logger.error("Error occurred: %s", str(e))
                return generate_response(
                    status=False,
                    payload={},
                    message=str(e),
                    status_code=400,
                )

            except Exception as e:
                logger.error("Unexpected error occurred: %s", str(e))
                return generate_response(
                    status=False,
                    payload={},
                    message=str(e),
                    status_code=500,
                )

        return wrapper

    return decorator


app = Bottle()


@app.route("/ping")
@safeguard()
def health_check() -> dict:
    """
    health-check endpoint
    """
    return {"result": "PONG"}


@app.route("/list-files", method=["OPTIONS", "POST"])
@safeguard()
def list_files() -> dict:
    """
    list_files endpoint
    """
    bucket_name: str = request.forms.bucket_name.strip()

    if bucket_name == "test_default":
        # set bucket name from environment variable
        bucket_name = os.getenv("BUCKET_NAME")

    # download files from bucket
    download_result = DownloadFiles(bucket_name=bucket_name).download_files()

    return download_result


@app.route("/download-file", methods=["GET"])
@safeguard(is_file_download=True)
def download_file() -> Any:
    """
    Download_file endpoint for serving file downloads to the client.
    It validates the requested file path and sends the file if available.
    """
    file_path = request.query.file_path.strip()

    # validate if file path is provided and exists
    if not file_path or not os.path.exists(file_path):
        return generate_response(
            status=False,
            payload={},
            message="File not found",
            status_code=404,
        )

    # set the Content-Disposition header to force download
    response.headers[
        "Content-Disposition"
    ] = f'attachment; filename="{os.path.basename(file_path)}"'

    # serve the file for download
    return static_file(file_path, root="/", mimetype="application/json", download=True)


if __name__ == "__main__":
    status = os.getenv("ENV") != "prod"
    bottle.debug(status)
    app.run(host="localhost", port=8080, reloader=status)
