# pylint: disable=import-error
"""
This is the starting point of the application
"""

import os
import boto3

# from utils import logger


class DownloadFiles:  # pylint: disable=too-few-public-methods
    """
    DownloadFiles Class
    """

    def __init__(self, bucket_name: str | None = None) -> None:
        """
        Constructor method
        """
        __session = boto3.Session()
        self.__s3 = __session.client("s3")
        self.__bucket_name: str = bucket_name

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
                print("➡ local_file_path:", local_file_path)
                file_list.append(local_file_path)
                break  # FIXME: remove this
        else:
            print(f"No files found in bucket {self.__bucket_name}.")
            # logger.warning(f"No files found in bucket {self.__bucket_name}.")
        return {"files": file_list}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    url = os.getenv("BUCKET_NAME")
    DownloadFiles(bucket_name=url).download_files()
