import websockets
from websockets.exceptions import ConnectionClosed,\
    InvalidHandshake, ProtocolError, InvalidURI


class WebSocket:
    def __init__(self, loop):
        self.loop = loop

    async def send(self, uri, data):
        """ Attempts to send data to given WebSocket. """

        try:
            async with websockets.connect(
                uri,
                timeout=3.0,
                loop=self.loop) \
                    as websocket:
                try:
                    await websocket.send(data)
                except (ConnectionClosed, InvalidHandshake,
                        ProtocolError, InvalidURI):
                    return False
                else:
                    await websocket.recv()
        except OSError:
            pass
