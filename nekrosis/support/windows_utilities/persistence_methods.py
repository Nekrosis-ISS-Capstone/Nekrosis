"""
persistence_methods.py: Windows specific persistence methods
"""

import enum


class WindowsPersistenceMethods(enum.Enum):
    """
    Windows-specific persistence methods.
    """

    REGEDIT_RUN: str = "Regedit Run Key"
