"""
linux.py: Linux-specific persistence logic.
"""

from support.core import Persistence


class LinuxPersistence(Persistence):
    """
    Linux-specific persistence logic.

    identifier: Effective user ID of the user to install the payload as.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        super().__init__(payload, identifier, custom_method)