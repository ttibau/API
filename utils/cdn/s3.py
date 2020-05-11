import aiobotocore

from settings import Config


class S3:
    def __init__(self):
        self.session = aiobotocore.get_session()

    async def upload(self, path_key, data, file_name):
        """  - path_key, key for path located in Config.cdn["paths"].
             - data, data to upload.
             - file_name, name of file to upload (including ext)
        """

        async with self.session.create_client(
            's3',
            region_name=Config.cdn["s3"]["region_name"],
            aws_secret_access_key=Config.cdn["s3"]["secret_access_key"],
            aws_access_key_id=Config.cdn["s3"]["access_key_id"],
            endpoint_url=Config.cdn["s3"]["endpoint_url"]
        ) as client:

            await client.put_object(
                Bucket=Config.cdn["bucket"],
                Key=Config.cdn["paths"][path_key].format(file_name),
                Body=data
            )
