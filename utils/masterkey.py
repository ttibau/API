import aiofiles
import secrets
import os


class MasterKey:
    def __init__(self, obj):
        self.obj = obj
        self.master_key_path = "{}/master_key.txt".format(obj.current_path)

    async def load(self):
        """ Attempts to load master key. """

        if os.path.exists(self.master_key_path):
            async with aiofiles.open(self.master_key_path, mode="r") as file:
                return await file.read()
        else:
            return await self.generate()

    async def generate(self):
        """ Generates master key file with key. """

        key = secrets.token_urlsafe(48)
        async with aiofiles.open(self.master_key_path, mode="w") as file:
            await file.write(key)

        return key
