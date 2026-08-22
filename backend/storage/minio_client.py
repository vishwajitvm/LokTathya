import os
import boto3
from botocore.exceptions import ClientError
from typing import Generator, Dict, Any, Optional
from tracenest import logger

class MinIOStorageService:
    """
    Priority 0: Production-grade MinIO Client wrapper.
    Ensures safe put, get, and metadata checks for raw document archiving.
    """
    
    def __init__(self):
        endpoint = os.environ.get("MINIO_ENDPOINT", "minio:9000")
        if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
            endpoint = f"http://{endpoint}"
            
        access_key = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
        secret_key = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
        
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1"
        )
        self.bucket = "loktathya-raw"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404':
                try:
                    self.client.create_bucket(Bucket=self.bucket)
                    logger.info("Created MinIO bucket", bucket=self.bucket)
                except Exception as ex:
                    logger.error("Failed to create MinIO bucket", bucket=self.bucket, error=str(ex))
            else:
                logger.error("Error checking MinIO bucket", bucket=self.bucket, error=str(e))

    def put(self, key: str, data: bytes, content_type: Optional[str] = None, metadata: Optional[Dict[str, str]] = None) -> bool:
        """
        Upload raw content to MinIO with custom metadata tags.
        """
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        if metadata:
            # S3 metadata keys are automatically prepended with x-amz-meta-
            extra_args["Metadata"] = {k: str(v) for k, v in metadata.items()}

        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                **extra_args
            )
            logger.info("Stored object in MinIO", key=key, size=len(data))
            return True
        except Exception as e:
            logger.error("Failed to store object in MinIO", key=key, error=str(e))
            return False

    def get(self, key: str) -> Optional[bytes]:
        """
        Retrieve raw content from MinIO.
        """
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            return response["Body"].read()
        except ClientError as e:
            if e.response.get('Error', {}).get('Code') == 'NoSuchKey':
                logger.warning("Object not found in MinIO", key=key)
            else:
                logger.error("Failed to get object from MinIO", key=key, error=str(e))
            return None
        except Exception as e:
            logger.error("Unknown error getting object from MinIO", key=key, error=str(e))
            return None

    def exists(self, key: str) -> bool:
        """
        Check if object exists in MinIO.
        """
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def stream(self, key: str, chunk_size: int = 65536) -> Generator[bytes, None, None]:
        """
        Stream raw content in chunks to avoid OOM for large documents.
        """
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            body = response["Body"]
            while True:
                chunk = body.read(chunk_size)
                if not chunk:
                    break
                yield chunk
        except Exception as e:
            logger.error("Failed to stream object from MinIO", key=key, error=str(e))
            raise

    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve object metadata headers.
        """
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=key)
            return {
                "content_type": response.get("ContentType"),
                "size": response.get("ContentLength"),
                "metadata": response.get("Metadata", {})
            }
        except ClientError:
            return None

    def delete_if_allowed(self, key: str) -> bool:
        """
        Delete object if permitted.
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info("Deleted object from MinIO", key=key)
            return True
        except Exception as e:
            logger.error("Failed to delete object from MinIO", key=key, error=str(e))
            return False
