"""
windows.py: Windows-specific persistence logic.
"""

from support.core import Persistence


class WindowsPersistence(Persistence):
    """
    Windows-specific persistence logic.
    """

    def __init__(self, payload: str, effective_user_id: int) -> None:
        super().__init__(payload, effective_user_id)