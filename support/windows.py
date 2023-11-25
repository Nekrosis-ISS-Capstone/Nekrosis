"""
windows.py: Windows-specific persistence logic.
"""

from support.core import Persistence


class WindowsPersistence(Persistence):
    """
    Windows-specific persistence logic.

    identifier: Security Identifier (SID) of the user to install the payload as.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        super().__init__(payload, identifier, custom_method)