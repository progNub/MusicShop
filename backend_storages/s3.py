import os
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3MediaStorage(S3Boto3Storage):

    def url(self, name, parameters=None, expire=None, http_method=None):

        MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
        MINIO_EXTERNAL_ENDPOINT = os.environ.get('MINIO_EXTERNAL_ENDPOINT')

        url = super(CustomS3MediaStorage, self).url(name, parameters, expire, http_method)
        if MINIO_EXTERNAL_ENDPOINT:
            url = url.replace(MINIO_ENDPOINT, MINIO_EXTERNAL_ENDPOINT)
        return url
