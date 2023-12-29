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

    # Requires System Integrity Protection to be lowered.
    LAUNCH_AGENT_SYSTEM:   str = "LaunchAgent - System"
    LAUNCH_DAEMON_SYSTEM:  str = "LaunchDaemon - System"

    # TODO: Implement following methods:
    # - Electron-based persistence ('ELECTRON_RUN_AS_NODE')