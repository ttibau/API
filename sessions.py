from settings import Config

from utils.server import Server
from utils.webhook import WebhookSend
from utils.websocket import WebSocket
from utils.cdn import Cdn
from utils.steam import Steam

from aioproxyio import proxy_io

from tables import Tables

from aiohttp_session import AIOHTTP


class Sessions:
    proxy = proxy_io(
        api_key=Config.proxyio["key"],
        session=AIOHTTP.ClientSession
    )
    websocket = WebSocket()
    webhook = WebhookSend()
    steam = Steam()
    database = Tables().database
    server = Server().load()
    cdn = Cdn().load()


SESSIONS = Sessions()
