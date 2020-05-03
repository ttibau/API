import aiob2

from settings import Config as config


class B2:
    def __init__(self, obj):
        client = aiob2.client(
            application_key_id=config.cdn["b2"]["application_key_id"],
            application_key=config.cdn["b2"]["application_key"],
            session=obj.sessions.aiohttp
        )

        self.bucket = client.bucket(bucket_id=config.cdn["bucket"])

    async def upload(self, path_key, data, file_name):
        """  - path_key, key for path located in Config.cdn["paths"].
             - data, data to upload.
             - file_name, name of file to upload (including ext)
        """

        await self.bucket.upload.data(
            data=data,
            file_name=config.cdn["paths"][path_key].format(file_name)
        )
