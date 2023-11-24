"""
macos.py: macOS-specific persistence logic.
"""

import enum

from support.core import Persistence


class MacPersistenceMethods(enum.Enum):
    """
    macOS-specific persistence methods.
    """

    LAUNCH_AGENT_USER    = "LaunchAgent - Current User"
    LAUNCH_AGENT_SYSTEM  = "LaunchAgent - System"
    LAUNCH_DAEMON_SYSTEM = "LaunchDaemon - System"


class MacPersistence(Persistence):
    """
    macOS-specific persistence logic.
    """

    def __init__(self, payload: str, effective_user_id: int, custom_method: str = None) -> None:
        super().__init__(payload, effective_user_id, custom_method)


    def _determine_recommended_persistence_method(self) -> str:
        """
        Determine the recommended persistence method for macOS.
        """
        if self.effective_user_id == 0:
            return MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value

        return MacPersistenceMethods.LAUNCH_AGENT_USER.value


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for macOS.
        """
        return [method.value for method in MacPersistenceMethods]