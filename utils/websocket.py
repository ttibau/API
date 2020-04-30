import websockets
from websockets.exceptions import ConnectionClosed,\
    InvalidHandshake, ProtocolError


class Webhook:
    def __init__(self, uri, data):
        self.url = uri
        self.data = data

    async def send(self):
        """ Attempts to send data to given webhook. """

        async with websockets.connect(self.url) as websocket:
            try:
                await websocket.send(self.data)
            except (ConnectionClosed, InvalidHandshake, ProtocolError):
                return False
            else:
                await websocket.recv()
