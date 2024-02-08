"""
permissions.py: Classifications for DOS permissions/privileges.
"""

import enum


class WindowsPrivilege(enum.Enum):
    """
    Unix permissions.
    """
    ADMINISTRATOR: int = 1
    STANDARD_USER: int = 0