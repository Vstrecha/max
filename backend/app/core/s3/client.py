"""
S3 client wrapper
Handles uploading files to an S3-compatible object storage.
"""

# --------------------------------------------------------------------------------

import boto3
from botocore.client import Config as BotoConfig
from botocore.exceptions import NoCredentialsError

# --------------------------------------------------------------------------------


class S3Client:
    """
    Wrapper around boto3 S3 client for file upload operations.
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket: str,
        endpoint_url: str,
        public_url: str,
        region: str = None,
    ):
        """
        Initialize S3 client with provided configuration.

        Args:
            access_key (str): S3 access key
            secret_key (str): S3 secret key
            bucket (str): S3 bucket name
            endpoint_url (str): S3 endpoint URL
            public_url (str): Public URL for accessing files
            region (str, optional): S3 region
        """
        # Check if S3 is configured
        if not all([access_key, secret_key, bucket, endpoint_url, public_url]):
            raise ValueError(
                "S3 configuration is incomplete. Please check your environment variables."
            )

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region,
            config=BotoConfig(signature_version="s3"),
        )
        self.bucket = bucket
        self.public_url = public_url

    # --------------------------------------------------------------------------------

    def upload_file(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        """
        Upload file to S3 and return public URL.

        Args:
            file_bytes (bytes): File content in bytes.
            filename (str): Original file name.
            content_type (str): MIME type of the file.

        Returns:
            str: Public URL to the uploaded file.

        Raises:
            Exception: If S3 credentials are missing.
        """
        unique_filename = f"avatars/{filename}"
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=unique_filename,
                Body=file_bytes,
                ContentType=content_type,
                ACL="public-read",
            )
            return f"{self.public_url}/{unique_filename}"
        except NoCredentialsError:
            raise Exception("S3 credentials not found")
