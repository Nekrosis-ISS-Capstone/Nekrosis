"""
persistence_methods.py: Windows specific persistence methods
"""

import enum


class WindowsPersistenceMethods(enum.Enum):
    """
    Windows-specific persistence methods.
    """

    REGEDIT_RUN:          str = "Regedit Run Key"
    STARTUP_CURRENT_USER: str = "Startup Folder (Current User)"
    STARTUP_GLOBAL:       str = "Startup Folder (Global)"