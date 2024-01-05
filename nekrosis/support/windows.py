"""
windows.py: Windows-specific persistence logic.
"""

from .base import Persistence


class WindowsPersistence(Persistence):
    """
    Windows-specific persistence logic.

    identifier: Security Identifier (SID) of the user to install the payload as.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        super().__init__(payload, identifier, custom_method)

        # Inherited from Persistence class:
        self.payload
        self.identifier
        self.custom_method
        self.temp_dir
        self.recommended_method

        super().__post_init__()


    def _determine_recommended_persistence_method(self) -> str:
        # TODO: Remove this line when the method is implemented.
        return super()._determine_recommended_persistence_method()


    def supported_persistence_methods(self) -> list:
        # TODO: Remove this line when the method is implemented.
        return super().supported_persistence_methods()


    def install(self) -> None:
        # TODO: Remove this line when the method is implemented.
        super().install()