import asyncio
from typing import List
import websockets
import json

from .types.models import Mixer, Patch, Status, IDType

from .commands import DaemonCommands, GoXLRCommands, StatusCommands

from .error import DaemonError, MixerNotFoundError


class Socket:
    """
    A class for handling the websocket connection to the daemon.
    It also handles the heartbeat task and the response queue. The response
    queue is used to ensure that the correct response is returned for a
    specific request.

    :param host: The host/IP address of the daemon.
    :param port: The port of the daemon.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.uri = f"ws://{self.host}:{self.port}/api/websocket"
        self.socket = None
        self.heartbeat_interval = 5
        self.heartbeat_task = None
        self.heartbeat_payload = {"id": 0, "data": "Ping"}
        self.response_queue = []

    async def connect(self):
        """
        Connects to the daemon and starts the heartbeat task.

        :return: True if the connection was successful, False otherwise.
        """
        self.socket = await websockets.connect(self.uri)
        self.heartbeat_task = asyncio.create_task(self.__send_heartbeat())
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

    async def receive(self, id: IDType | int = None):
        """
        Waits for a response from the daemon. If an ID is specified, it will
        wait until it receives a response with the same ID and queue all other
        responses.

        :param id: The ID of the response to wait for. If not specified, it
                   will wait for the first response and will not add it to
                   the queue.

        :return: The response from the daemon.

        :raises: `DaemonError` if the daemon returns an error.
        """
        if not id:
            response = await self.socket.recv()
            response = json.loads(response)
            return response
        elif isinstance(id, IDType):
            id = id.value

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

    async def receive_patch(self) -> List[Patch]:
        """
        Helper method to wait for a patch message from the daemon.

        :return: The patch from the daemon.
        """
        response = await self.receive(IDType.Patch)
        patches = response.get("data").get("Patch")

        return [Patch(p) for p in patches]

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


class GoXLR(Socket, DaemonCommands, GoXLRCommands, StatusCommands):
    """
    A class for interacting with the GoXLR Utility daemon.
    """

    def __init__(self, host="localhost", port=14564, serial=None):
        super().__init__(host, port)

        self.status: Status = None

        self.mixer: Mixer = None  # the currently selected mixer
        self.serial: str = (
            serial  # shorthand for self.mixer.hardware_info.serial_number
        )

    async def ping(self):
        """
        Pings the GoXLR Utility daemon.

        :return: "Ok" if the daemon is running.
        """
        return await self.send("Ping")

    async def update(self):
        """
        Gets the latest data from the GoXLR Utility daemon and updates the status
        and mixers attributes.

        :return: The status of the daemon.

        :raises DaemonError: If the daemon is not running.
        :raises MixerNotFoundError: If the specified mixer is not found.

        :note: This method is automatically called when the class is instantiated.
            You should manually call this method periodically to ensure that the data
            is up to date.
        """
        self.status = await self.get_status()

        if self.serial:
            self.mixer = self.select_mixer(self.serial)

        return self.status

    async def receive_patch(self, update: bool = True) -> List[Patch]:
        """
        Helper method to wait for a patch message from the daemon.

        :param update: Whether or not to update the status and mixers attributes
                       after receiving the patch.

        :return: The patch from the daemon.
        """

        patches = await Socket.receive_patch(self)

        if update:
            await self.update()

        return patches

    def select_mixer(self, serial: str = None):
        """
        Chooses a mixer to interact with.

        :param serial: The serial number of the mixer to interact with.
                       If not specified, it will default to the first mixer.

        :return: The selected mixer.

        :raises DaemonError: If no mixers are found.
        :raises MixerNotFoundError: If the specified mixer is not found.
        """

        # set self.serial to serial if specified. if None, default to first mixer
        if not self.status.mixers:
            raise DaemonError("No mixers found.")

        if serial:
            if serial not in self.status.mixers:
                raise MixerNotFoundError(f"Mixer with serial {serial} not found")
        else:
            serial = next(iter(self.status.mixers))

        self.serial = serial
        self.mixer = self.status.mixers.get(self.serial)

        return self.mixer

    async def connect(self):
        """
        Connects to the GoXLR Utility daemon and gets the latest data.

        :return: True if the connection was successful, False otherwise.

        :raises DaemonError: If no mixers are found.
        """
        connected = await super().connect()
        if connected:
            await self.update()
            self.select_mixer()  # select the first mixer by default

        return connected
