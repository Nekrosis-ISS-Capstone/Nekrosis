"""
persistence_methods.py: macOS-specific persistence methods.
"""
import enum


class MacPersistenceMethods(enum.Enum):
    """
    macOS-specific persistence methods.
    """

    LAUNCH_AGENT_USER:     str = "LaunchAgent - Current User"

    # Requires root access.
    LAUNCH_AGENT_LIBRARY:  str = "LaunchAgent - Library"
    LAUNCH_DAEMON_LIBRARY: str = "LaunchDaemon - Library"

    # TODO: Implement following methods:
    # - Root volume persistence.
    # - Electron-based persistence ('ELECTRON_RUN_AS_NODE')