from google.cloud import storage
from google.auth import load_credentials_from_file
from config.config import settings

class GCSClient():
    def __init__(self):
        # Load credentials from JSON file
        # credentials, _ = load_credentials_from_file(settings.GCS_CREDENTIALS_JSON)
        self.client = storage.Client()
        self.bucket = self.client.bucket(settings.GCS_BUCKET_NAME)

    def upload_file(self, source_file_path: str, destination_blob_name: str):
        """
        Uploads a file to the GCS bucket.
        :param source_file_path: Path to the file on the local file system
        :param destination_blob_name: The name for the file in GCS
        :return: Public URL of the uploaded file
        """
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)
        blob.make_public()  # Make the file public if you need public access
        return blob.public_url

    def download_file(self, blob_name: str, destination_file_path: str):
        """
        Downloads a file from the GCS bucket.
        :param blob_name: The name of the file in GCS
        :param destination_file_path: Path where the file should be saved locally
        """
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(destination_file_path)

    def delete_file(self, blob_name: str):
        """
        Deletes a file from the GCS bucket.
        :param blob_name: The name of the file in GCS
        """
        blob = self.bucket.blob(blob_name)
        blob.delete()
