import aiobotocore

from settings import CONFIG


class S3:
    def __init__(self):
        self.session = aiobotocore.get_session()

    async def upload(self, path_key, data, file_name):
        """  - path_key, key for path located in CONFIG.cdn["paths"].
             - data, data to upload.
             - file_name, name of file to upload (including ext)
        """

        async with self.session.create_client(
            's3',
            region_name=CONFIG.cdn["s3"]["region_name"],
            aws_secret_access_key=CONFIG.cdn["s3"]["secret_access_key"],
            aws_access_key_id=CONFIG.cdn["s3"]["access_key_id"],
            endpoint_url=CONFIG.cdn["s3"]["endpoint_url"]
        ) as client:

            await client.put_object(
                Bucket=CONFIG.cdn["bucket"],
                Key=CONFIG.cdn["paths"][path_key].format(file_name),
                Body=data
            )
