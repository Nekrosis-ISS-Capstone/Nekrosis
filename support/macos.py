"""
macos.py: macOS-specific persistence logic.
"""
import platform

from support.core import Persistence
from support.macos_utilities.launch_service import LaunchService
from support.macos_utilities.persistence_methods import MacPersistenceMethods

if platform.system() == "Darwin":
    import py_sip_xnu
else:
    py_sip_xnu = None


class MacPersistence(Persistence):
    """
    macOS-specific persistence logic.

    identifier: Effective user ID of the user to install the payload as.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        super().__init__(payload, identifier, custom_method)

        # Inherited from Persistence class:
        self.payload
        self.identifier
        self.custom_method
        self.temp_dir
        self.recommended_method

        self.xnu_version = self._get_xnu_version()


    def _get_xnu_version(self) -> int:
        """
        Get major XNU version.
        """
        return int(platform.release().split(".")[0])


    def _determine_recommended_persistence_method(self) -> str:
        """
        Determine the recommended persistence method for macOS.
        """
        # If we lack root access, we can only use user-level persistence methods.
        if self.identifier != 0:
            return MacPersistenceMethods.LAUNCH_AGENT_USER.value

        return MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for macOS.
        """
        methods = [method.value for method in MacPersistenceMethods]
        if self.identifier != 0:
            methods.remove(MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value)
            methods.remove(MacPersistenceMethods.LAUNCH_AGENT_LIBRARY.value)

        return methods


    def install(self) -> None:
        """
        Install payload.
        """
        method = self.configured_persistence_method()

        if method in [
            MacPersistenceMethods.LAUNCH_AGENT_USER.value,
            MacPersistenceMethods.LAUNCH_AGENT_LIBRARY.value,
            MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value
        ]:
            LaunchService(self.payload).install_generic_launch_service(method)
            return

        raise NotImplementedError(f"Method {method} not implemented.")