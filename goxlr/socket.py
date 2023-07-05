import asyncio
import websockets
import json

from .commands import *

from .error import DaemonError


class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.uri = f"ws://{self.host}:{self.port}/api/websocket"
        self.socket = None
        self.heartbeat_interval = 5
        self.heartbeat_task = None
        self.heartbeat_payload = {"id": 1, "data": "Ping"}
        self.serial = None

    async def connect(self):
        self.socket = await websockets.connect(self.uri)
        self.heartbeat_task = asyncio.create_task(self.__send_heartbeat())

        status = await self.send("GetStatus")
        mixers = status.get("Status").get("mixers")
        if mixers:
            # get first key, why would there be more than one?
            self.serial = next(iter(mixers))
        else:
            raise DaemonError("No mixers found")

        return self.socket.open

    async def __send_heartbeat(self):
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            await self.socket.send(json.dumps(self.heartbeat_payload))

    async def send(self, payload):
        payload = {"id": 1, "data": payload}
        await self.socket.send(json.dumps(payload))

        response = await self.receive()
        data = response.get("data")

        if data == "Ok":
            return data
        elif isinstance(data, dict):
            if data.get("Status") or data.get("Patch"):
                return data
            if data.get("Error"):
                raise DaemonError(data.get("Error"))

    async def receive(self):
        response = await self.socket.recv()
        return json.loads(response)

    async def open(self):
        return await self.connect()

    async def close(self):
        await self.socket.close()
        self.heartbeat_task.cancel()
        return self.socket.closed

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()


class GoXLR(Socket, GeneralCommands, DaemonCommands, GoXLRCommands):
    """
    Bundles all functions across all command classes into one class. Inherits from Socket.
    It is recommended to use this class instead of Socket.
    """

    def __init__(self, host="localhost", port=14564):
        super().__init__(host, port)
