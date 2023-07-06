import asyncio
import time
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
        self.heartbeat_payload = {"id": 0, "data": "Ping"}
        self.response_queue = []
        self.serial = None

    async def connect(self):
        """
        Connects to the daemon and starts the heartbeat task.

        :return: True if the connection was successful, False otherwise.
        """
        self.socket = await websockets.connect(self.uri)
        self.heartbeat_task = asyncio.create_task(self.__send_heartbeat())

        status = await self.send("GetStatus")
        mixers = status.get("mixers")
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

    async def send(self, payload, id=None):
        """
        Sends a payload to the daemon and waits for a response.

        :param payload: The payload to send to the daemon.
        :param id: The ID of the payload. If not specified, it will
                   automatically generate one. Used purely for identifying
                   the correct response, considering that this is an async
                   function and responses may come in out of order.

        :return: The response from the daemon.
        """
        id = id or self.response_queue[-1].get("id") + 1 if self.response_queue else 1

        payload = {"id": id, "data": payload}
        await self.socket.send(json.dumps(payload))

        response = await self.receive(id)
        data = response.get("data")

        if data == "Ok":
            return data
        elif isinstance(data, dict):
            if status := data.get("Status"):
                return status
            elif patch := data.get("Patch"):
                return patch
            elif error := data.get("Error"):
                raise DaemonError(error)

    async def receive(self, id=None):
        """
        Waits for a response from the daemon. If an ID is specified, it will
        wait until it receives a response with the same ID and queue all other
        responses.

        If no ID is specified, it will wait for the first response and will
        not add it to the queue.

        To specifically wait for a heartbeat response, specify an ID of 0.
        To specifically wait for a patch response, specify an ID of 2**64 - 1.

        :param id: The ID of the response to wait for.

        :return: The response from the daemon.
        """
        if not id:
            response = await self.socket.recv()
            response = json.loads(response)
            return response

        # if we already have the response, return it
        for r in self.response_queue:
            if r.get("id") == id:
                self.response_queue.remove(r)
                return r

        # keep receiving until we get a response with the same id
        while True:
            response = await self.socket.recv()
            response = json.loads(response)

            if response.get("id") == id:
                return response
            else:
                if response.get("id") in (0, 2**64 - 1):
                    # no need to queue heartbeat and patch responses
                    # if we want to do something with them, either specify
                    # the id or don't specify one at all
                    continue
                self.response_queue.append(response)

    async def open(self):
        """
        Alias for `connect()`.

        :return: True if the connection was successful, False otherwise.
        """
        return await self.connect()

    async def close(self):
        """
        Closes the connection to the daemon.

        :return: True if the connection was closed, False otherwise.
        """
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
