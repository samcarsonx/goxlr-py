from ..error import DaemonError, MixerNotFoundError
from ..types.models import HttpSettings, LogLevel, Mixer, PathType, Status


class StatusCommands:
    """
    Commands related to getting the status of the GoXLR.
    I decided to split this into its own file because there's
    already enough code in goxlr.py.
    """

    def __init__(self):
        self.status: Status = None

    async def get_status(self) -> Status:
        """
        Returns the status of the GoXLR.

        :return: The status of the GoXLR.

        :raises DaemonError: If the status could not be retrieved.

        :note: You should use GoXLR.update() instead of this method.
        """
        status = await self.send("GetStatus")

        if not status:
            raise DaemonError("Failed to get status from daemon.")

        return Status(status)

    def get_http_settings(self) -> HttpSettings:
        """
        :return: The HTTP settings of the GoXLR.
        """
        return self.status.config.http_settings

    def get_daemon_version(self) -> str:
        """
        :return: The version of the GoXLR Utility daemon.
        """
        return self.status.config.daemon_version

    def is_autostart_enabled(self) -> bool:
        """
        :return: Whether or not the GoXLR Utility daemon is set to start on boot.
        """
        return self.status.config.autostart_enabled

    def is_tray_icon_visible(self) -> bool:
        """
        :return: Whether or not the GoXLR Utility daemon is set to show a tray icon.
        """
        return self.status.config.show_tray_icon

    def is_tts_enabled(self) -> bool:
        """
        :return: Whether or not TTS is enabled.
        """
        return self.status.config.tts_enabled

    def is_network_access_allowed(self) -> bool:
        """
        :return: Whether or not network access is allowed.
        """
        return self.status.config.allow_network_access

    def get_log_level(self) -> LogLevel:
        """
        :return: The log level of the GoXLR Utility daemon.
        """
        return self.status.config.log_level

    def get_mixer(self, serial: str = None) -> Mixer:
        """
        Returns a mixer object with the specified serial number.

        :param serial: The serial number of the mixer to interact with.
                          If not specified, it will default to the currently selected mixer.

        :return: The requested mixer object.

        :raises MixerNotFoundError: If the specified mixer is not found.
        """
        if not serial:
            return self.mixer  # return the currently selected mixer

        if serial not in self.status.mixers:
            raise MixerNotFoundError(f"Mixer {serial} not found.")

        return self.status.mixers.get(serial)

    def get_path(self, path: PathType) -> str:
        """
        Returns the path of the specified path type.

        :param path: The path type to get the path of.

        :return: The path of the specified path type.

        :raises ValueError: If the specified path type is invalid.
        """
        match path:
            case PathType.Profiles:
                return self.status.files.profiles
            case PathType.MicProfiles:
                return self.status.files.mic_profiles
            case PathType.Samples:
                return self.status.files.samples
            case PathType.Presets:
                return self.status.files.presets
            case PathType.Icons:
                return self.status.files.icons
            case PathType.Logs:
                return self.status.files.logs
            case _:
                raise ValueError(f"Invalid path type: {path}")

    def get_files(self, path: PathType) -> list:
        """
        Returns the files of the specified path type.

        :param path: The path type to get the files of.

        :return: The files of the specified path type.

        :raises ValueError: If the specified path type is invalid.
        """
        match path:
            case PathType.Profiles:
                return self.status.files.profiles_files
            case PathType.MicProfiles:
                return self.status.files.mic_profiles
            case PathType.Samples:
                return self.status.files.samples
            case PathType.Presets:
                return self.status.files.presets
            case PathType.Icons:
                return self.status.files.icons
            case _:
                raise ValueError(f"Invalid path type: {path}")
