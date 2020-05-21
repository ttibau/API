import aiohttp


class Sessions:
    ClientSession = aiohttp.ClientSession()


AIOHTTP = Sessions()
