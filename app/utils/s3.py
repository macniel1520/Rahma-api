import asyncio
from io import BytesIO

from minio import Minio

from app.utils.structlog_config import logger
from app.core.config import settings

log = logger.bind(module=__name__, service="s3")


class AsyncMinioClient:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = True,
    ):
        """Initialize AsyncMinioClient for S3-compatible storage operations.

        Args:
            endpoint: S3 server endpoint (e.g., "localhost:9000" or "https://s3.example.com)
            access_key: S3 access key for authentication
            secret_key: S3 secret key for authentication
            secure: Whether to use HTTPS connection (defaults to True)
        """
        from urllib.parse import urlparse

        log.info(f"Initializing S3 client with endpoint={endpoint}")
        parsed = urlparse(endpoint)

        self.client = Minio(
            parsed.netloc,
            access_key=access_key,
            secret_key=secret_key,
            secure=(parsed.scheme == "https") if parsed.scheme else secure,
        )
        self.bucket = bucket

    async def upload_file(self, file_bytes: bytes, object_name: str) -> str:
        """Asynchronously upload a file to S3-compatible storage.

        Args:
            file_bytes: File content as bytes
            object_name: Name/key for the object in the bucket

        Returns:
            The object name/key of the uploaded file

        Raises:
            RuntimeError: If the specified bucket does not exist
        """
        log.info(f"[upload_file] Upload request, size={len(file_bytes)} bytes")
        return await asyncio.to_thread(self._upload_file_sync, file_bytes, object_name)

    def _upload_file_sync(self, file_bytes: bytes, object_name: str) -> str:
        log.info(f"[_upload_file_sync] Uploading to bucket={self.bucket}")
        if not self.client.bucket_exists(self.bucket):
            raise RuntimeError(f"Bucket '{self.bucket}' не существует")

        self.client.put_object(
            self.bucket,
            object_name,
            data=BytesIO(file_bytes),
            length=len(file_bytes),
            content_type="image/jpeg",
        )

        log.info(f"[_upload_file_sync] Successfully uploaded object={object_name}")
        return object_name


minio_client = AsyncMinioClient(
    endpoint=settings.s3.s3_endpoint,
    access_key=settings.s3.s3_access_key,
    secret_key=settings.s3.s3_secret_key,
    secure=settings.s3.s3_secure,
    bucket=settings.s3.s3_bucket,
)
