"""
persistence_methods.py: Linux specific persistence methods
"""

import enum


class LinuxPersistenceMethods(enum.Enum):
    """
    Linux-specific persistence methods.
    """

    CRONJOB_USER: str = "Cronjob - Current User"
    CRONJOB_ROOT: str = "Cronjob - Root"