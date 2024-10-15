# pylint: disable=import-error
"""
This is the starting point of the application
"""

import os
import sys
import argparse
from typing import Optional
import boto3
import botocore
from botocore.client import Config
from utils import logger


class DownloadFiles:
    """
    DownloadFiles Class
    """

    def __init__(self, bucket_name: Optional[str] = None) -> None:
        """
        Constructor method
        """
        self.__bucket_name: str = bucket_name
        __session = boto3.Session()
        self.__s3 = __session.client(
            "s3", config=Config(signature_version=botocore.UNSIGNED)
        )
        self.__validate_data()

    def __validate_data(self):
        """
        Validate provided data and returns True if the data is properly validated else returns False
        """
        __is_valid: bool = True

        if not self.__bucket_name:
            msg = "No bucket name found!"
            # logger.fatal(msg)
            raise ValueError(msg)

        return __is_valid

    def parse_arguments(self):
        """
        This parses the command line arguments, assigns them to the respective instance variables,
        validates them and then calls the function associated  with the provided method name.
        """
        parser = argparse.ArgumentParser(
            description="All the operations related to project management using Asana"
        )
        parser.add_argument(
            "-bn", "--bucket_name", type=str, help="AWS S3 bucket name", required=True
        )
        args = parser.parse_args()
        if args.bucket_name:
            self.__bucket_name = args.bucket_name

        if not self.__validate_data():
            sys.exit(1)

    # TODO: Add validation layer
    def download_files(self):
        """
        download_files internally call __download_files method
        """
        return self.__download_files()

    def __download_files(self):
        """
        This method download files from provided destination
        """
        # the current working directory
        __root_path = os.getcwd()

        # defining the path for temp_downloads
        __temp_downloads_path = os.path.join(__root_path, "temp_downloads")

        # creating the temp_downloads folder if not exist
        os.makedirs(__temp_downloads_path, exist_ok=True)

        response = self.__s3.list_objects_v2(Bucket=self.__bucket_name)
        file_list = []
        if "Contents" in response:
            for obj in response["Contents"]:
                file_key = obj["Key"]
                local_file_path = os.path.join(__temp_downloads_path, file_key)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                self.__s3.download_file(self.__bucket_name, file_key, local_file_path)
                file_list.append(local_file_path)
            logger.debug(
                f"{len(file_list)} files downloaded from bucket {self.__bucket_name}."
            )
        else:
            print(f"No files found in bucket {self.__bucket_name}.")
            logger.warning(f"No files found in bucket {self.__bucket_name}.")
        return {"files": file_list}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    __bucket_name = os.getenv("BUCKET_NAME")
    __download_files = DownloadFiles(bucket_name=__bucket_name)
    __download_files.parse_arguments()
    downloaded_files = __download_files.download_files()
    print("➡ Downloaded Files:", downloaded_files)
