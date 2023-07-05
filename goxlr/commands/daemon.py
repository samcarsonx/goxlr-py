from ..types import LogLevel, PathType


class DaemonCommands:
    async def __send_daemon(self, payload):
        payload = {"Daemon": payload}
        return await self.send(payload)

    async def open_ui(self):
        return await self.__send_daemon("OpenUi")

    async def activate(self):
        return await self.__send_daemon("Activate")

    async def stop_daemon(self):
        return await self.__send_daemon("StopDaemon")

    async def open_path(self, pathType: PathType):
        return await self.__send_daemon({"OpenPath": pathType.name})

    async def set_log_level(self, logLevel: LogLevel):
        return await self.__send_daemon({"SetLogLevel": logLevel.name})

    async def set_show_tray_icon(self, enabled: bool):
        return await self.__send_daemon({"SetShowTrayIcon": enabled})

    async def set_tts_enabled(self, enabled: bool):
        return await self.__send_daemon({"SetTTSEnabled": enabled})

    async def set_auto_start_enabled(self, enabled: bool):
        return await self.__send_daemon({"SetAutoStartEnabled": enabled})

    async def set_allow_network_access(self, enabled: bool):
        return await self.__send_daemon({"SetAllowNetworkAccess": enabled})

    async def recover_defaults(self, pathType: PathType):
        return await self.__send_daemon({"RecoverDefaults": pathType.name})
