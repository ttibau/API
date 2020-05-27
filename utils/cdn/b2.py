import aiob2

from settings import CONFIG

from aiohttp_session import AIOHTTP


class B2:
    def __init__(self):
        client = aiob2.client(
            application_key_id=CONFIG.cdn["b2"]["application_key_id"],
            application_key=CONFIG.cdn["b2"]["application_key"],
            session=AIOHTTP.ClientSession
        )

        self.bucket = client.bucket(bucket_id=CONFIG.cdn["bucket"])

    async def upload(self, path_key, data, file_name):
        """  - path_key, key for path located in CONFIG.cdn["paths"].
             - data, data to upload.
             - file_name, name of file to upload (including ext)
        """

        await self.bucket.upload.data(
            data=data,
            file_name=CONFIG.cdn["paths"][path_key].format(file_name)
        )
