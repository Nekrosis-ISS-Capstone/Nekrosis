"""
permissions.py: Classifications for Unix permissions/privileges.
"""

import enum


class UnixPrivilege(enum.Enum):
    """
    Unix permissions.
    """
    ROOT: int = 0