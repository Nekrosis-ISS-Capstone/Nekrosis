"""
windows.py: Windows-specific persistence logic.
"""

from support.core import Persistence


class WindowsPersistence(Persistence):
    """
    Windows-specific persistence logic.
    """

    def __init__(self, payload: str, effective_user_id: int, custom_method: str = None) -> None:
        super().__init__(payload, effective_user_id, custom_method)