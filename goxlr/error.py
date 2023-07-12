class DaemonError(Exception):
    """
    Raised when the GoXLR Utility returns an 'Error' message.
    """

    pass


class MixerNotFoundError(Exception):
    """
    Raised when a given mixer does not exist.
    """

    pass


class MissingFeatureError(Exception):
    """
    Raised when a feature is not available on the GoXLR Mini.
    """

    pass
