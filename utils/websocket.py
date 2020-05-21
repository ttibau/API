import websockets
from websockets.exceptions import ConnectionClosed,\
    InvalidHandshake, ProtocolError, InvalidURI


class WebSocket:
    async def send(self, uri, data):
        """ Attempts to send data to given WebSocket. """

        try:
            async with websockets.connect(
                uri,
                timeout=3.0) \
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
