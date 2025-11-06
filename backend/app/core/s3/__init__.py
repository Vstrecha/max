"""
S3 API client for shared use
Provides S3 client that can be used across all bot applications.
"""

# --------------------------------------------------------------------------------

from .client import S3Client

# --------------------------------------------------------------------------------


def create_s3_client(
    access_key: str,
    secret_key: str,
    bucket: str,
    endpoint_url: str,
    public_url: str,
    region: str = None,
) -> S3Client:
    """
    Create S3 client with specified configuration.

    Args:
        access_key (str): S3 access key
        secret_key (str): S3 secret key
        bucket (str): S3 bucket name
        endpoint_url (str): S3 endpoint URL
        public_url (str): Public URL for accessing files
        region (str, optional): S3 region

    Returns:
        S3Client: Configured S3 client
    """
    return S3Client(
        access_key=access_key,
        secret_key=secret_key,
        bucket=bucket,
        endpoint_url=endpoint_url,
        public_url=public_url,
        region=region,
    )


# --------------------------------------------------------------------------------

__all__ = ["S3Client", "create_s3_client"]
