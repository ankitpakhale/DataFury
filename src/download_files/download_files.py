# pylint: disable=import-error
"""
This is the starting point of the application
"""

import os
from dotenv import load_dotenv
import boto3

load_dotenv()

BUCKET_NAME: str = os.getenv("BUCKET_NAME")
DOWNLOAD_PATH: str = os.getenv("DOWNLOAD_PATH")


class DownloadFiles:  # pylint: disable=too-few-public-methods
    """
    DownloadFiles Class
    """

    def __init__(self) -> None:
        """
        Constructor method
        """
        __session = boto3.Session()
        self.__s3 = __session.client("s3")

    def download_files(
        self, bucket_name: str, download_path: str = ".././downloaded_files"
    ) -> None:
        """
        This method download files from provided destination
        """
        bucket_name = bucket_name.strip()

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        response = self.__s3.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            for obj in response["Contents"]:
                file_key = obj["Key"]
                file_path = os.path.join(download_path, file_key)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                print(f"Downloading {file_key} to {file_path}")
                self.__s3.download_file(bucket_name, file_key, file_path)
        else:
            print(f"No files found in bucket {bucket_name}.")


if __name__ == "__main__":
    download_files_obj = DownloadFiles()
    download_files_obj.download_files(
        bucket_name=BUCKET_NAME, download_path=DOWNLOAD_PATH
    )
