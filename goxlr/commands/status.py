from ..error import DaemonError, MixerNotFoundError
from ..types.models import HttpSettings, LogLevel, Mixer, PathType


class StatusCommands:
    """
    Commands related to getting the status of the GoXLR.
    I decided to split this into its own file because there's
    already enough code in goxlr.py.
    """

    async def get_status(self):
        """
        Returns the status of the GoXLR. `GoXLR.update()` should be used instead.
        """
        status = await self.send("GetStatus")

        if not status:
            raise DaemonError("Failed to get status from daemon.")

        return status

    def get_http_settings(self) -> HttpSettings:
        return self.config.http_settings

    def get_daemon_version(self) -> str:
        return self.config.get("daemon_version")

    def is_autostart_enabled(self) -> bool:
        return self.config.get("autostart_enabled")

    def is_tray_icon_visible(self) -> bool:
        return self.config.get("show_tray_icon")

    def is_tts_enabled(self) -> bool:
        return self.config.get("tts_enabled")

    def is_network_access_allowed(self) -> bool:
        return self.config.get("allow_network_access")

    def get_log_level(self) -> LogLevel:
        return LogLevel[self.config.get("log_level")]

    def get_mixer(self, serial: str = None) -> Mixer:
        if not serial:
            return self.mixer  # return the currently selected mixer

        if serial not in self.mixers:
            raise MixerNotFoundError(f"Mixer {serial} not found.")

        return Mixer(self.mixers.get(serial))

    def get_path(self, path: PathType) -> str:
        index = path.name.lower()

        # Profiles -> profile
        # Mic profiles -> mic_profile
        # Samples -> samples

        match path:
            case PathType.Profiles:
                index = "profile"
            case PathType.MicProfiles:
                index = "mic_profile"
            case _:
                pass

        return self.paths.get(index + "_directory")

    def get_files(self, path: PathType) -> list:
        if path == PathType.MicProfiles:  # MicProfiles -> mic_profiles
            return self.files.get("mic_profiles")
        return self.files.get(path.name.lower())
