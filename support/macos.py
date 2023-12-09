"""
macos.py: macOS-specific persistence logic.
"""

import enum
import platform

from support.core import Persistence

# Only import py_sip_xnu if we're running on macOS.
try:
    import py_sip_xnu
except ImportError:
    py_sip_xnu = None


class MacPersistenceMethods(enum.Enum):
    """
    macOS-specific persistence methods.
    """

    LAUNCH_AGENT_USER     = "LaunchAgent - Current User"
    LAUNCH_AGENT_LIBRARY  = "LaunchAgent - Library"
    LAUNCH_DAEMON_LIBRARY = "LaunchDaemon - Library"

    if py_sip_xnu and py_sip_xnu.SipXnu().sip_object.can_edit_root:
        LAUNCH_AGENT_SYSTEM   = "LaunchAgent - System"
        LAUNCH_DAEMON_SYSTEM  = "LaunchDaemon - System"


class MacPersistence(Persistence):
    """
    macOS-specific persistence logic.

    identifier: Effective user ID of the user to install the payload as.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        super().__init__(payload, identifier, custom_method)

        self.xnu_version = self._get_xnu_version()


    def _get_xnu_version(self) -> str:
        """
        Get major XNU version.
        """
        return platform.release().split(".")[0]


    def _determine_recommended_persistence_method(self) -> str:
        """
        Determine the recommended persistence method for macOS.
        """
        # If we lack root access, we can only use user-level persistence methods.
        if self.identifier != 0:
            return MacPersistenceMethods.LAUNCH_AGENT_USER.value

        if "LaunchDaemon - System" in self.supported_persistence_methods():
            return MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value

        return MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for macOS.
        """
        return [method.value for method in MacPersistenceMethods]