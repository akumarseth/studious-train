from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
import os
from os.path import exists
from src.config import config
from loguru import logger


class Azure_helper:
    
    def __init__(self):
        try:
            self.account = config.az_detail["STORAGE_ACCOUNT_NAME"]
            self.key = config.az_detail["ACCOUNT_KEY"]
            self.container_name = config.az_detail["MODEL_CONTAINER_NAME"]
            self.connect_str = config.az_detail["CONNECTION_STRING"]

            self.blob_service_client = BlobServiceClient.from_connection_string(conn_str=config.az_detail["CONNECTION_STRING"])
        except Exception as e:
             print(str(e))

    def download_model_to_local_dir(self):
        try:

            blob_name = 'model_data.pkl'
            current_dir = os.path.dirname(os.path.abspath(__file__))
            local_model_path = os.path.join(current_dir, blob_name)

            is_file_exists = exists(local_model_path)
            if is_file_exists:
                logger.info(f"file {blob_name} is already availble in local directory {current_dir} so skipping the download.")
                return local_model_path

            logger.info(f"file {blob_name} download is started... ")
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(blob_name)

            # Download Blob
            with open(local_model_path, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())
                
            logger.info(f"file {blob_name} download is completed... ")
            return local_model_path

        except Exception as e:
            logger.info(e)
