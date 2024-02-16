"""
persistence_methods.py: macOS-specific persistence methods.
"""

import enum


class MacPersistenceMethods(enum.Enum):
    """
    macOS-specific persistence methods.
    """

    LAUNCH_AGENT_USER:     str = "LaunchAgent - Current User"

    # Requires vulnerable electron application
    LAUNCH_AGENT_ELECTRON: str = "LaunchAgent - Electron"

    # Requires root access.
    LAUNCH_AGENT_LIBRARY:  str = "LaunchAgent - Library"
    LAUNCH_DAEMON_LIBRARY: str = "LaunchDaemon - Library"

    # Requires System Integrity Protection to be lowered.
    LAUNCH_AGENT_SYSTEM:   str = "LaunchAgent - System"
    LAUNCH_DAEMON_SYSTEM:  str = "LaunchDaemon - System"

    # Requires root access.
    CRONJOB_USER:          str = "Cronjob - Current User"
    CRONJOB_ROOT:          str = "Cronjob - Root"