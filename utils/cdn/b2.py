import aiob2

from settings import Config

from aiohttp_session import AIOHTTP


class B2:
    def __init__(self):
        client = aiob2.client(
            application_key_id=Config.cdn["b2"]["application_key_id"],
            application_key=Config.cdn["b2"]["application_key"],
            session=AIOHTTP.ClientSession
        )

        self.bucket = client.bucket(bucket_id=Config.cdn["bucket"])

    async def upload(self, path_key, data, file_name):
        """  - path_key, key for path located in Config.cdn["paths"].
             - data, data to upload.
             - file_name, name of file to upload (including ext)
        """

        await self.bucket.upload.data(
            data=data,
            file_name=Config.cdn["paths"][path_key].format(file_name)
        )
